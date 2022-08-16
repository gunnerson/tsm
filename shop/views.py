from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import FieldError
# from django.db import IntegrityError

from .models import Order, Part, Job, OrderPart, Purchase, \
    PurchaseItem, Balance, PartPlace, PartType, Shelf, OrderTime, ShelfGroup, \
    Core
from invent.models import Truck, Trailer, Company
from .forms import OrderForm, JobForm, PartForm, PurchaseForm, BalanceForm, \
    PartPlaceForm, PartTypeForm, ShelfForm, PartUpdateForm, ShelfGroupForm, \
    CoreForm
from .utils import get_job_forms, get_part_forms, get_purchase_forms, \
    link_with_part
from .mixins import ObjectView, FormSetView
from users.mixins import ReadCheckMixin, WriteCheckMixin, AdminCheckMixin
from users.models import AccountVar
from invent.gomotive import get_vehicles_locations
from users.utils import write_check


class OrderListView(ReadCheckMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        if self.request.GET.get('closed', None):
            qs = self.model.objects.all()
        else:
            qs = self.model.objects.filter(closed=None)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.GET.get('closed', None):
            context['closed'] = True
        context['btn_new'] = True
        context['filter_bar'] = True
        context['create_url'] = 'shop:create_order'
        return context


class OrderView(ReadCheckMixin, ObjectView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_form.html'

    def form_valid(self, form):
        self.object = form.save()
        try:
            if self.object.mileage is None:
                data = get_vehicles_locations(self.object.truck.kt_id)
                self.object.mileage = data['odometer']
                self.object.save(update_fields=['mileage'])
        except (AttributeError, ValueError, KeyError):
            pass
        if not self.is_create:
            checks = self.request.POST.getlist('checks[]')
            assigned_only = True if 'assigned_only' in checks else False
            job_formset = get_job_forms(self.object, self.request.POST)
            if assigned_only:
                part_formset = get_part_forms(self.object, self.request.POST)
            else:
                part_formset = get_part_forms(
                    self.object, self.request.POST, exclude=False)
            if job_formset.is_valid() and part_formset.is_valid():
                for f in job_formset:
                    inst = f.save(commit=False)
                    if inst.amount == 0:
                        try:
                            inst.delete()
                        except AssertionError:
                            pass
                    elif inst.job_id:
                        inst.order = self.object
                        inst.save()
                for f in part_formset:
                    inst = f.save(commit=False)
                    inst.order = self.object
                    if not inst.id and inst.part_id:
                        if inst.part.stock >= inst.amount:
                            inst.save()
                            inst.part.stock -= inst.amount
                            inst.part.save(update_fields=['stock'])
                            link_with_part(inst)
                            return redirect(self.object.get_absolute_url())
                        else:
                            f.add_error('amount', 'Not enough in stock')
                            return self.render_to_response(
                                self.get_context_data(
                                    form=form,
                                    job_formset=job_formset,
                                    part_formset=part_formset,
                                ))
                    elif inst.id and inst.part_id:
                        before_inst = OrderPart.objects.get(id=inst.id)
                        if before_inst.part.id == inst.part_id:
                            inst.part.stock -= inst.amount - before_inst.amount
                            inst.part.save(update_fields=['stock'])
                            if inst.amount == 0:
                                try:
                                    inst.delete()
                                except AssertionError:
                                    pass
                            else:
                                inst.save()
                                link_with_part(inst)
                if not assigned_only:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            job_formset=job_formset,
                            part_formset=get_part_forms(
                                self.object, self.request.POST, exclude=False),
                            assigned_only=False),
                    )
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, job_formset=job_formset,
                                          part_formset=part_formset))
        return redirect(self.object.get_absolute_url())

    def get_context_data(
            self, *args, job_formset=None, part_formset=None, assigned_only=True, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            order = self.get_object()
            total_clocked = 0
            for ordertime in order.ordertime_set.all():
                total_clocked += ordertime.total
            context['clocked_in'] = order.ordertime_set.exclude(start=None)
            context['total_clocked'] = total_clocked
            context['total_billed'] = order.labor_total
            context['total_parts'] = order.parts_total(self.request.user)
            context['inst_id'] = order.id
            context['job_formset'] = (
                job_formset if job_formset else get_job_forms(order))
            if assigned_only:
                context['assigned_only'] = True
            context['part_formset'] = (
                part_formset if part_formset else get_part_forms(order))
            context['btn_budget'] = True
            context['budget_url'] = 'shop:order_budget'
            context['btn_print'] = True
            context['print_url'] = 'shop:order_print'
            context['btn_image'] = True
            if order.truck:
                context['image_url'] = 'docs:truck_image'
                context['image_id'] = order.truck.id
                context['is_truck'] = True
            else:
                context['image_url'] = 'docs:trailer_image'
                context['image_id'] = order.trailer.id
                context['is_trailer'] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_create=self.is_create)
        truck_ids = []
        trailer_ids = []
        if self.is_create:
            qs = Truck.objects.filter(show=True)
            for q in qs:
                if q.order_set.filter(closed=None):
                    truck_ids.append(q.id)
            kwargs.update(trucks=qs.exclude(id__in=truck_ids))
            qs = Trailer.objects.filter(show=True)
            for q in qs:
                if q.order_set.filter(closed=None):
                    trailer_ids.append(q.id)
            kwargs.update(trailers=qs.exclude(id__in=trailer_ids))
        return kwargs


class OrderPrintView(ReadCheckMixin, DetailView):
    model = Order
    template_name = 'shop/order_print.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        order = self.get_object()
        parts_total = order.parts_total(user)
        tax_rate = float(AccountVar.objects.get(name="SALES_TAX").value) / 100
        header_id = int(AccountVar.objects.get(name="INVOICE_HEADER").value)
        labor_rate = int(AccountVar.objects.get(name="LABOR_RATE").value)
        context['shop_header'] = Company.objects.get(id=header_id)
        context['parts_total'] = parts_total
        context['tax'] = float(parts_total) * tax_rate
        context['labor_total'] = order.labor_total * labor_rate
        context['total'] = float(parts_total) + \
            context['tax'] + float(context['labor_total'])
        return context


class JobFormSetView(ReadCheckMixin, FormSetView):
    model = Job
    form_class = JobForm
    detail_url = 'shop:job_part_types'
    fields = ('name', 'man_hours')
    field_names = ('Description', 'Man-hours')


class PartPlaceFormSetView(ReadCheckMixin, FormSetView):
    model = PartPlace
    form_class = PartPlaceForm
    fields = ('part', 'side_left', 'side_right', 'axle_str', 'axle_drv',
              'axle_add', 'axle_trl',)
    field_names = ('Part', 'Left side', 'Right side', 'STR axle', 'DRV axle',
                   'ADD axle', 'TRL axle', )

    def get_queryset(self):
        if self.kwargs['unit'] == 'truck':
            unit = Truck.objects.get(id=self.kwargs['pk'])
            qs = self.model.objects.filter(truck=unit)
        else:
            unit = Trailer.objects.get(id=self.kwargs['pk'])
            qs = self.model.objects.filter(trailer=unit)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.kwargs['unit'] == 'truck':
            unit = Truck.objects.get(id=self.kwargs['pk'])
            context['to_truck'] = unit
        else:
            unit = Trailer.objects.get(id=self.kwargs['pk'])
            context['to_trailer'] = unit
        context['assign'] = True
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_modelformset(request.POST)
        if formset.is_valid():
            if self.kwargs['unit'] == 'truck':
                unit = Truck.objects.get(id=self.kwargs['pk'])
                for f in formset:
                    inst = f.save(commit=False)
                    try:
                        part = inst.part
                        inst.truck = unit
                        inst.save()
                    except ObjectDoesNotExist:
                        inst.delete()
            else:
                unit = Trailer.objects.get(id=self.kwargs['pk'])
                for f in formset:
                    inst = f.save(commit=False)
                    try:
                        part = inst.part
                        inst.trailer = unit
                        inst.save()
                    except ObjectDoesNotExist:
                        inst.delete()
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs['unit'] == 'truck':
            unit = Truck.objects.get(id=self.kwargs['pk'])
        else:
            unit = Trailer.objects.get(id=self.kwargs['pk'])
        qs = unit.partplace_set.all()
        exclude_ids = []
        for q in qs:
            if q.part.id not in exclude_ids:
                exclude_ids.append(q.part.id)
        kwargs.update(exclude=exclude_ids)
        return kwargs


class JobPartListView(ReadCheckMixin, ListView):
    model = Part
    template_name = 'shop/jobpart_add.html'
    query = None

    def get_queryset(self):
        self.query = self.request.GET.get('query', None)
        if self.query:
            qs = self.model.objects.search(self.query, 'Part')
        else:
            qs = self.model.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        job = Job.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(*args, **kwargs)
        if self.query:
            context['query'] = self.query
        qs = self.get_queryset()
        context['checked'] = []
        for q in qs:
            if q in job.parts.all():
                context['checked'].append(q.id)
        context['btn_save'] = True
        context['search_bar'] = True
        return context

    def post(self, *args, **kwargs):
        job = Job.objects.get(id=kwargs['pk'])
        qs = self.get_queryset()
        for q in qs:
            if self.request.POST.get(str(q.id), None):
                job.parts.add(q)
            else:
                job.parts.remove(q)
        return redirect('.')


class JobPartTypeListView(ReadCheckMixin, ListView):
    model = PartType
    template_name = 'shop/jobparttype_add.html'

    def get_context_data(self, *args, **kwargs):
        job = Job.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        context['checked'] = []
        for q in qs:
            if q in job.part_types.all():
                context['checked'].append(q.id)
        context['btn_save'] = True
        return context

    def post(self, *args, **kwargs):
        job = Job.objects.get(id=kwargs['pk'])
        qs = self.get_queryset()
        for q in qs:
            if self.request.POST.get(str(q.id), None):
                job.part_types.add(q)
            else:
                job.part_types.remove(q)
        return redirect('.')


class PartTypeFormSetView(ReadCheckMixin, FormSetView):
    model = PartType
    form_class = PartTypeForm
    fields = ('name', )
    field_names = ('Type',)


class PartFormSetView(ReadCheckMixin, FormSetView):
    model = Part
    form_class = PartForm
    search_bar = True
    filter_bar = True
    detail_url = 'shop:part'
    fields = ('part_number', 'part_type', 'name', 'stock', 'price',)
    field_names = ('Part number', 'Type', 'Description',
                   'In Stock', 'Re-sale price', )

    def get_queryset(self):
        show_all = self.request.GET.get('show_all', None)
        query = self.request.GET.get('query', None)
        part_type = self.request.GET.get('part_type', None)
        if query or part_type:
            qs = self.model.objects.all()
            if part_type:
                qs = self.model.objects.filter(part_type__name=part_type)
            if query:
                qs = self.model.objects.search(
                    query,
                    self.model.__name__,
                )
        elif show_all:
            qs = self.model.objects.all()
        else:
            qs = self.model.objects.none()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        part_types = []
        pts = PartType.objects.all()
        for p in pts:
            part_types.append(p.name)
        context['part_types'] = part_types
        if self.request.GET.get('query', None) or self.request.GET.get('part_type', None):
            context['show_all'] = True
        else:
            context['show_all'] = self.request.GET.get('show_all', False)
        return context


class PartDetailView(ReadCheckMixin, DetailView):
    model = Part

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        part = self.get_object()
        purchases = PurchaseItem.objects.filter(part=part)
        context['purchases'] = purchases
        orders = OrderPart.objects.filter(part=part)
        context['orders'] = orders
        context['replaces'] = part.replaces.all()
        context['replaces2'] = part.part_set.all()
        try:
            context['replaces3'] = part.part_set.last(
            ).replaces.exclude(id=part.id)
        except AttributeError:
            pass
        return context


class PartUpdateView(AdminCheckMixin, UpdateView):
    model = Part
    form_class = PartUpdateForm
    template_name = 'shop/edit_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        return context


class PurchaseListView(ReadCheckMixin, ListView):
    model = Purchase
    template_name = 'shop/purchase_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_new'] = True
        context['create_url'] = 'shop:create_purchase'
        return context


class PurchaseView(ReadCheckMixin, ObjectView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'shop/purchase_form.html'

    def form_valid(self, form):
        self.object = form.save()
        try:
            truck = form.cleaned_data['truck']
        except KeyError:
            truck = None
        try:
            trailer = form.cleaned_data['trailer']
        except KeyError:
            trailer = None
        if not self.is_create:
            formset = get_purchase_forms(self.object, self.request.POST)
            if formset.is_valid():
                parts_surcharge = (int(AccountVar.objects.get(
                    name='PARTS_SURCHARGE').value) / 100) + 1
                for f in formset:
                    inst = f.save(commit=False)
                    inst.purchase = self.object
                    if not inst.id and inst.part_id:
                        inst.save()
                        inst.part.stock += inst.amount
                        inst.part.save(update_fields=['stock'])
                        if not inst.part.price:
                            inst.part.price = 0
                        if (float(inst.price) * parts_surcharge) > inst.part.price:
                            inst.part.price = float(
                                inst.price) * parts_surcharge
                            inst.part.save(update_fields=['price'])
                    elif inst.id and inst.part_id:
                        before_inst = PurchaseItem.objects.get(id=inst.id)
                        inst.part.stock += inst.amount - before_inst.amount
                        inst.part.save(update_fields=['stock'])
                        if not inst.part.price:
                            inst.part.price = 0
                        if (float(inst.price) * parts_surcharge) > inst.part.price:
                            inst.part.price = float(
                                inst.price) * parts_surcharge
                            inst.part.save(update_fields=['price'])
                        if inst.amount == 0:
                            try:
                                inst.delete()
                            except AssertionError:
                                pass
                        else:
                            inst.save()
                    if truck:
                        try:
                            truck_place, created = PartPlace.objects.get_or_create(
                                part=inst.part,
                                truck=truck,
                            )
                        except ObjectDoesNotExist:
                            pass
                    elif trailer:
                        try:
                            trailer_place, created = PartPlace.objects.get_or_create(
                                part=inst.part,
                                trailer=trailer,
                            )
                        except ObjectDoesNotExist:
                            pass
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset))
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            purchase = self.get_object()
            purchaseitems = purchase.purchaseitem_set.all()
            parts_total = 0
            for p in purchaseitems:
                if p.price and p.amount:
                    parts_total += (p.price * p.amount)
            context['parts_total'] = parts_total
            context['btn_budget'] = True
            context['budget_url'] = 'shop:purchase_budget'
            context['inst_id'] = purchase.id
            context['formset'] = (
                formset if formset else get_purchase_forms(purchase))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_create=self.is_create)
        return kwargs


class BalanceFormSetView(ReadCheckMixin, FormSetView):
    model = Balance
    form_class = BalanceForm
    fields = ('date', 'category', 'total', 'comments')
    field_names = ('Date', 'Category', 'Total', 'Comments')
    filter_bar = True

    def get_queryset(self):
        today = date.today()
        this_year = today.year
        last_year = this_year - 1
        this_month = today.month
        last_month = this_month - 1
        category = self.request.GET.get('category', None)
        if category:
            qs = self.model.objects.filter(category=category)
        else:
            qs = self.model.objects.all()
        show = self.request.GET.get('show', 'show_this_month')
        if show == 'show_this_month':
            qs = qs.filter(
                date__year=this_year, date__month=this_month)
        elif show == 'show_last_month':
            if this_month != 1:
                qs = qs.filter(
                    date__year=this_year, date__month=last_month)
            else:
                qs = qs.filter(
                    date__year=last_year, date__month=12)
        elif show == 'show_last_quarter':
            first_quarter = [1, 2, 3]
            second_quarter = [4, 5, 6]
            third_quarter = [7, 8, 9]
            fourth_quarter = [10, 11, 12]
            if this_month in first_quarter:
                last_quarter = fourth_quarter
            elif this_month in second_quarter:
                last_quarter = first_quarter
            elif this_month in third_quarter:
                last_quarter = second_quarter
            else:
                last_quarter = third_quarter
            if last_quarter != fourth_quarter:
                qs = qs.filter(
                    date__year=this_year, date__month__in=last_quarter)
            else:
                qs = qs.filter(
                    date__year=last_year, date__month__in=last_quarter)
        elif show == 'show_last_year':
            qs = qs.filter(date__year=last_year)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        running_total = 0
        total_tools = 0
        total_parts = 0
        total_building = 0
        total_supplies = 0
        total_salaries = 0
        total_income = 0
        today = date.today()
        this_month = today.month
        last_month = this_month - 1
        for q in qs:
            running_total += q.total
            if q.category == 'T':
                total_tools += q.total
            elif q.category == 'P':
                total_parts += q.total
            elif q.category == 'E':
                total_supplies += q.total
            elif q.category == 'S':
                total_salaries += q.total
            elif q.category == 'I':
                total_income += q.total
            elif q.category == 'B':
                total_building += q.total
        this_month_labor = 0
        last_month_labor = 0
        total_labor = 0
        qs2 = Order.objects.all()
        for q in qs2:
            try:
                labor_rate = int(AccountVar.objects.get(
                    name="LABOR_RATE").value)
                if q.closed.month == this_month:
                    this_month_labor += q.labor_total * labor_rate
                    total_labor += q.labor_total * labor_rate
                elif ((q.closed.month == last_month) or
                      (this_month == 1 and q.closed.month == 12)):
                    last_month_labor += q.labor_total * labor_rate
                    total_labor += q.labor_total * labor_rate
                else:
                    total_labor += q.labor_total * labor_rate
            except AttributeError:
                pass
        context['show'] = self.request.GET.get('show', 'show_this_month')
        context['selected_category'] = self.request.GET.get('category', None)
        context['running_total'] = running_total
        context['total_tools'] = total_tools
        context['total_parts'] = total_parts
        context['total_building'] = total_building
        context['total_supplies'] = total_supplies
        context['total_salaries'] = total_salaries
        context['total_income'] = total_income
        context['this_month_labor'] = this_month_labor
        context['last_month_labor'] = last_month_labor
        context['total_labor'] = total_labor
        return context


def budget_invoice(request, pk):
    order = Order.objects.get(id=pk)
    user = request.user
    parts_total = order.parts_total(user)
    tax_rate = float(AccountVar.objects.get(name="SALES_TAX").value) / 100
    tax = float(parts_total) * tax_rate
    labor_rate = int(AccountVar.objects.get(name="LABOR_RATE").value)
    labor_total = order.labor_total * labor_rate
    total = float(parts_total) + tax + float(labor_total)
    check_existing = Balance.objects.filter(
        date=order.closed,
        category='I',
        total=total,
        comments=order,
    )
    if not check_existing and order.closed:
        Balance(
            date=order.closed,
            category='I',
            total=total,
            comments=order,
        ).save()
    return redirect(order.get_absolute_url())


def budget_purchase(request, pk):
    purchase = Purchase.objects.get(id=pk)
    check_existing = Balance.objects.filter(
        date=purchase.date,
        category='P',
        total=-purchase.total,
        comments=purchase,
    )
    if not check_existing and purchase.total:
        Balance(
            date=purchase.date,
            category='P',
            total=-purchase.total,
            comments=purchase,
        ).save()
    return redirect(purchase.get_absolute_url())


def assign_to_all(request, pk, unit):
    part = Part.objects.get(id=pk)
    if unit == 'truck':
        trucks = Truck.objects.all()
        for t in trucks:
            try:
                PartPlace.objects.get(part=part, truck=t)
            except ObjectDoesNotExist:
                PartPlace(part=part, truck=t).save()
    else:
        trailers = Trailer.objects.all()
        for t in trailers:
            try:
                PartPlace.objects.get(part=part, trailer=t)
            except ObjectDoesNotExist:
                PartPlace(part=part, trailer=t).save()
    return redirect('users:profile', new_profile.id)


def order_stop(request, pk):
    ordertime = OrderTime.objects.get(id=pk)
    ordertime.get_total()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ShelfGroupListView(ReadCheckMixin, ListView):
    model = ShelfGroup
    template_name = 'shop/shelves.html'


class ShelfGroupCreateView(AdminCheckMixin, CreateView):
    model = ShelfGroup
    template_name = 'shop/edit_form.html'


class ShelfCreateView(AdminCheckMixin, CreateView):
    model = Shelf
    form_class = ShelfForm
    template_name = 'shop/edit_form.html'
    success_url = reverse_lazy('shop:shelves')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        group = ShelfGroup.objects.get(id=self.kwargs['pk'])
        kwargs.update(group=group)
        return kwargs


class ShelfUpdateView(AdminCheckMixin, UpdateView):
    model = Shelf
    form_class = ShelfForm
    template_name = 'shop/edit_form.html'
    success_url = reverse_lazy('shop:shelves')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(group=self.object.group)
        return kwargs


def shelfgroup_up(request, pk):
    group1 = ShelfGroup.objects.get(id=pk)
    num1 = group1.order_number
    num2 = num1 - 1
    if num2 >= 0:
        try:
            group2 = ShelfGroup.objects.get(order_number=num2)
            group2.order_number += 1
            group2.save(update_fields=['order_number'])
        except ObjectDoesNotExist:
            pass
        group1.order_number -= 1
        group1.save(update_fields=['order_number'])
    return redirect('shop:shelves')


def shelfgroup_down(request, pk):
    group1 = ShelfGroup.objects.get(id=pk)
    num1 = group1.order_number
    num2 = num1 + 1
    try:
        group2 = ShelfGroup.objects.get(order_number=num2)
        group2.order_number -= 1
        group2.save(update_fields=['order_number'])
    except ObjectDoesNotExist:
        pass
    group1.order_number += 1
    group1.save(update_fields=['order_number'])
    return redirect('shop:shelves')


class CoreFormSetView(ReadCheckMixin, FormSetView):
    model = Core
    form_class = CoreForm
    template_name = 'shop/purchase_cores.html'
    fields = ('part', 'amount', 'price')
    field_names = ('Part', 'Amount', 'Price')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        purchase = Purchase.objects.get(id=self.kwargs['pk'])
        items = purchase.purchaseitem_set.all()
        part_ids = []
        for item in items:
            part_ids.append(item.part.id)
        parts = Part.objects.filter(id__in=part_ids)
        kwargs.update(parts=parts)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['purchase'] = Purchase.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_modelformset(request.POST)
        purchase = Purchase.objects.get(id=self.kwargs['pk'])
        if formset.is_valid() and write_check(request.user):
            for f in formset:
                inst = f.save(commit=False)
                inst.purchase = purchase
                inst.save()
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))
