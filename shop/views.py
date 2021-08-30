from django.shortcuts import redirect
from django.views.generic import ListView

from .models import Order, Part, Job, OrderPart, Purchase, PurchaseItem
from .forms import OrderForm, JobForm, PartForm, OrderPartForm, PurchaseForm, PurchaseItemForm
from .utils import get_job_forms, get_part_forms, get_purchase_forms
from .mixins import ObjectView, FormSetView
from users.mixins import ReadCheckMixin, WriteCheckMixin


class OrderListView(ReadCheckMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        return self.model.objects.filter(closed=None)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_custom'] = True
        context['page_title'] = 'Work orders'
        context['nav_link'] = 'Orders'
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
                    if inst.amount == 0:
                        try:
                            inst.delete()
                        except AssertionError:
                            pass
                    elif inst.part_id:
                        inst.order = self.object
                        inst.save()
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, job_formset=job_formset,
                                          part_formset=part_formset))
        return redirect(self.object.get_absolute_url())

    def get_context_data(
            self, *args, job_formset=None, part_formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        if self.is_create:
            context['page_title'] = 'Create new work order'
            context['nav_link'] = 'New order'
        else:
            order = self.get_object()
            context['page_title'] = 'Update ' + order.__str__()
            context['nav_link'] = 'Update order'
            context['job_formset'] = (
                job_formset if job_formset else get_job_forms(order))
            context['part_formset'] = (
                part_formset if part_formset else get_part_forms(order))
        return context


class JobFormSetView(WriteCheckMixin, FormSetView):
    model = Job
    form_class = JobForm
    page_title = 'List of standart jobs'
    nav_link = 'Jobs'
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
        context['btn_back'] = True
        context['btn_save'] = True
        context['filter_bar'] = True
        context['page_title'] = 'Add parts'
        context['nav_link'] = 'Parts'
        return context

    def post(self, *args, **kwargs):
        job = Job.objects.get(id=kwargs['pk'])
        qs = self.get_queryset()
        for q in qs:
            if self.request.POST.get(str(q.id), None):
                job.parts.add(q)
            else:
                job.parts.remove(q)
        return redirect('./parts')


class PartFormSetView(WriteCheckMixin, FormSetView):
    model = Part
    form_class = PartForm
    page_title = 'List of parts'
    nav_link = 'Parts'
    filter_bar = True
    fields = ('part_number', 'name', 'stock', 'stock_unit')
    field_names = ('Part number', 'Description', 'In Stock', 'Units')


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
                    if inst.amount == 0:
                        try:
                            inst.delete()
                        except AssertionError:
                            pass
                    elif inst.part_id:
                        inst.order = self.object
                        inst.save()
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset))
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, formset=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        if self.is_create:
            context['page_title'] = 'Create new purchase order'
            context['nav_link'] = 'New purchase'
        else:
            order = self.get_object()
            context['page_title'] = 'Update ' + order.__str__()
            context['nav_link'] = 'Update order'
            context['formset'] = (
                formset if formset else get_purchase_forms(order))
        return context
