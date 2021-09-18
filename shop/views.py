from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from datetime import date
from django.db import IntegrityError

from .models import Order, OrderTime, Part, Job, OrderPart, Purchase, \
    PurchaseItem, Balance, Inspection
from invent.models import Truck, Trailer
from .forms import OrderForm, JobForm, PartForm, PurchaseForm, BalanceForm, \
    InspectionForm
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
        else:
            OrderTime(order=self.object).save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(
            self, *args, job_formset=None, part_formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            order = self.get_object()
            context['total_clocked'] = order.ordertime.total
            context['total_billed'] = order.labor_total
            context['total_parts'] = order.parts_total(self.request.user)
            context['inst_id'] = order.id
            context['job_formset'] = (
                job_formset if job_formset else get_job_forms(order))
            context['part_formset'] = (
                part_formset if part_formset else get_part_forms(order))
            context['btn_print'] = True
            context['print_url'] = 'shop:order_print'
            context['btn_image'] = True
            if order.truck:
                context['image_url'] = 'docs:truck_image'
                context['image_id'] = order.truck.id
            else:
                context['image_url'] = 'docs:trailer_image'
                context['image_id'] = order.trailer.id
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
    detail_url = 'shop:job_parts'
    fields = ('name', 'man_hours')
    field_names = ('Description', 'Man-hours')


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


class PartFormSetView(WriteCheckMixin, FormSetView):
    model = Part
    form_class = PartForm
    search_bar = True
    fields = ('part_number', 'name', 'stock', 'stock_unit')
    field_names = ('Part number', 'Description', 'In Stock', 'Units')


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
                    elif inst.id and inst.part_id:
                        before_inst = PurchaseItem.objects.get(id=inst.id)
                        inst.part.stock += inst.amount - before_inst.amount
                        inst.part.save(update_fields=['stock'])
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        running_total = 0
        this_month = 0
        last_month = 0
        today = date.today()
        for q in qs:
            running_total += q.total
            if q.date.month == today.month:
                this_month += q.total
            elif q.date.month == today.month - 1:
                last_month += q.total
        context['running_total'] = running_total
        context['this_month'] = this_month
        context['last_month'] = last_month
        return context


class InspectionListView(ReadCheckMixin, ListView):
    model = Inspection
    template_name = 'shop/inspection_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_new'] = True
        context['create_url'] = 'shop:create_inspection'
        return context


class InspectionView(WriteCheckMixin, ObjectView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'shop/inspection_form.html'

    def get_context_data(
            self, *args, job_formset=None, part_formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        if not self.is_create:
            inst = self.get_object()
            context['inst_id'] = inst.id
            context['btn_image'] = True
            if inst.truck:
                context['image_url'] = 'docs:truck_image'
                context['image_id'] = inst.truck.id
            else:
                context['image_url'] = 'docs:trailer_image'
                context['image_id'] = inst.trailer.id
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_create=self.is_create)
        return kwargs
