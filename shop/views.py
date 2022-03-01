from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
# from django.db import IntegrityError

from .models import Order, Part, Job, OrderPart, Purchase, \
    PurchaseItem, Balance, PartPlace, PartType
from invent.models import Truck, Trailer
from .forms import OrderForm, JobForm, PartForm, PurchaseForm, BalanceForm, \
    PartPlaceForm
from .utils import get_job_forms, get_part_forms, get_purchase_forms, \
    link_with_part
from .mixins import ObjectView, FormSetView
from users.mixins import ReadCheckMixin, WriteCheckMixin


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


class OrderView(WriteCheckMixin, ObjectView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_form.html'

    def form_valid(self, form):
        self.object = form.save()
        if not self.is_create:
            job_formset = get_job_forms(self.object, self.request.POST)
            part_formset = get_part_forms(self.object, self.request.POST)
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
                        inst.part.stock -= inst.amount - before_inst.amount
                        inst.part.save(update_fields=['stock'])
                        if inst.amount == 0:
                            try:
                                link_with_part(inst, True)
                                inst.delete()
                            except AssertionError:
                                pass
                        else:
                            inst.save()
                            link_with_part(inst)
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, job_formset=job_formset,
                                          part_formset=part_formset))
        # else:
        #     OrderTime(order=self.object).save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(
            self, *args, job_formset=None, part_formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            order = self.get_object()
            total_clocked = 0
            for ordertime in order.ordertime_set.all():
                total_clocked += ordertime.total
            context['total_clocked'] = total_clocked
            context['total_billed'] = order.labor_total
            context['total_parts'] = order.parts_total(self.request.user)
            context['inst_id'] = order.id
            context['job_formset'] = (
                job_formset if job_formset else get_job_forms(order))
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
            qs = Truck.objects.all()
            for q in qs:
                if q.order_set.filter(closed=None):
                    truck_ids.append(q.id)
            kwargs.update(trucks=qs.exclude(id__in=truck_ids))
            qs = Trailer.objects.all()
            for q in qs:
                if q.order_set.filter(closed=None):
                    trailer_ids.append(q.id)
            kwargs.update(trailers=qs.exclude(id__in=trailer_ids))
        return kwargs


class OrderPrintView(WriteCheckMixin, DetailView):
    model = Order
    template_name = 'shop/order_print.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        order = self.get_object()
        parts_total = order.parts_total(user)
        context['parts_total'] = parts_total
        context['tax'] = parts_total * user.profile.tax
        context['labor_total'] = order.labor_total * user.profile.labor_rate
        context['total'] = parts_total + \
            context['tax'] + context['labor_total']
        return context


class JobFormSetView(WriteCheckMixin, FormSetView):
    model = Job
    form_class = JobForm
    detail_url = 'shop:job_part_types'
    fields = ('name', 'man_hours')
    field_names = ('Description', 'Man-hours')


class PartPlaceFormSetView(WriteCheckMixin, FormSetView):
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
                    if f.has_changed():
                        inst = f.save(commit=False)
                        inst.truck = unit
                        inst.save()
            else:
                unit = Trailer.objects.get(id=self.kwargs['pk'])
                for f in formset:
                    if f.has_changed():
                        inst = f.save(commit=False)
                        inst.trailer = unit
                        inst.save()
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))


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


class JobPartTypeListView(WriteCheckMixin, ListView):
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


class PartFormSetView(WriteCheckMixin, FormSetView):
    model = Part
    form_class = PartForm
    search_bar = True
    detail_url = 'shop:part'
    fields = ('part_number', 'part_type', 'name', 'stock', 'price',)
    field_names = ('Part number', 'Type', 'Description',
                   'In Stock', 'Re-sale price', )


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
        context['replaces3'] = part.part_set.last().replaces.all()
        return context


class PurchaseListView(ReadCheckMixin, ListView):
    model = Purchase
    template_name = 'shop/purchase_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_new'] = True
        context['create_url'] = 'shop:create_purchase'
        return context


class PurchaseView(WriteCheckMixin, ObjectView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'shop/purchase_form.html'

    def form_valid(self, form):
        self.object = form.save()
        if not self.is_create:
            formset = get_purchase_forms(self.object, self.request.POST)
            if formset.is_valid():
                for f in formset:
                    inst = f.save(commit=False)
                    inst.purchase = self.object
                    if not inst.id and inst.part_id:
                        inst.save()
                        inst.part.stock += inst.amount
                        inst.part.save(update_fields=['stock'])
                        if (float(inst.price) * 1.15) > inst.part.price:
                            inst.part.price = float(inst.price) * 1.15
                            inst.part.save(update_fields=['price'])
                    elif inst.id and inst.part_id:
                        before_inst = PurchaseItem.objects.get(id=inst.id)
                        inst.part.stock += inst.amount - before_inst.amount
                        inst.part.save(update_fields=['stock'])
                        if (float(inst.price) * 1.15) > inst.part.price:
                            inst.part.price = float(inst.price) * 1.15
                            inst.part.save(update_fields=['price'])
                        if inst.amount == 0:
                            try:
                                inst.delete()
                            except AssertionError:
                                pass
                        else:
                            inst.save()
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset))
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            order = self.get_object()
            context['btn_budget'] = True
            context['budget_url'] = 'shop:purchase_budget'
            context['inst_id'] = order.id
            context['formset'] = (
                formset if formset else get_purchase_forms(order))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_create=self.is_create)
        return kwargs


class BalanceFormSetView(WriteCheckMixin, FormSetView):
    model = Balance
    form_class = BalanceForm
    fields = ('date', 'category', 'total', 'comments')
    field_names = ('Date', 'Category', 'Total', 'Comments')
    filter_bar = True

    def get_queryset(self):
        today = date.today()
        show = self.request.GET.get('show', 'show_this_month')
        if show == 'show_this_month':
            qs = Balance.objects.filter(
                date__year=today.year, date__month=today.month)
        elif show == 'show_last_month':
            if today.month != 1:
                qs = Balance.objects.filter(
                    date__year=today.year, date__month=today.month - 1)
            else:
                qs = Balance.objects.filter(
                    date__year=today.year - 1, date__month=12)
        else:
            qs = Balance.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = Balance.objects.all()
        running_total = 0
        total_tools = 0
        total_parts = 0
        total_building = 0
        total_supplies = 0
        total_salaries = 0
        total_income = 0
        this_month = 0
        this_month_income = 0
        this_month_salaries = 0
        last_month = 0
        last_month_income = 0
        last_month_salaries = 0
        today = date.today()
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
            if q.date.month == today.month and q.date.year == today.year:
                this_month += q.total
                if q.category == 'I':
                    this_month_income += q.total
                elif q.category == 'S':
                    this_month_salaries += q.total
            elif ((q.date.month == today.month - 1 and q.date.year == today.year)
                  or (today.month == 1 and q.date.month == 12 and q.date.year == today.year - 1)):
                last_month += q.total
                if q.category == 'I':
                    last_month_income += q.total
                elif q.category == 'S':
                    last_month_salaries += q.total
        this_month_labor = 0
        last_month_labor = 0
        qs2 = Order.objects.all()
        for q in qs2:
            try:
                if q.closed.month == today.month:
                    this_month_labor += q.labor_total * 100
                elif ((q.closed.month == today.month - 1) or
                      (today.month == 1 and q.closed.month == 12)):
                    last_month_labor += q.labor_total * 100
            except AttributeError:
                pass
        context['show'] = self.request.GET.get('show', 'show_this_month')
        context['running_total'] = running_total
        context['total_tools'] = total_tools
        context['total_parts'] = total_parts
        context['total_building'] = total_building
        context['total_supplies'] = total_supplies
        context['total_salaries'] = total_salaries
        context['total_income'] = total_income
        context['this_month'] = this_month
        context['this_month_income'] = this_month_income
        context['this_month_salaries'] = this_month_salaries
        context['last_month'] = last_month
        context['last_month_income'] = last_month_income
        context['last_month_salaries'] = last_month_salaries
        context['this_month_labor'] = this_month_labor
        context['last_month_labor'] = last_month_labor
        return context


def budget_invoice(request, pk):
    order = Order.objects.get(id=pk)
    user = request.user
    parts_total = order.parts_total(user)
    tax = parts_total * user.profile.tax
    labor_total = order.labor_total * user.profile.labor_rate
    total = parts_total + tax + labor_total
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
    return redirect(part.get_absolute_url())