from django.shortcuts import redirect
from django.views.generic import ListView

from .models import Order, Part, Job, OrderPart
from .forms import OrderForm, JobForm, OrderPartForm
from .utils import get_job_forms
from .mixins import ObjectView, FormSetView
from users.mixins import ReadCheckMixin, WriteCheckMixin


class OrderListView(ReadCheckMixin, ListView):
    model = Order
    template_name = 'shop/list.html'

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
    template_name = 'shop/form.html'

    def form_valid(self, form):
        self.object = form.save()
        if not self.is_create:
            formset = get_job_forms(self.object, self.request.POST)
            if formset.is_valid():
                for f in formset:
                    inst = f.save(commit=False)
                    if inst.amount == 0:
                        inst.delete()
                    elif inst.job_id:
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
            context['page_title'] = 'Create new work order'
            context['nav_link'] = 'New order'
        else:
            order = self.get_object()
            context['page_title'] = 'Update order ' + order.__str__()
            context['nav_link'] = 'Update order'
            context['formset'] = formset if formset else get_job_forms(order)
        return context


class JobFormSetView(WriteCheckMixin, FormSetView):
    model = Job
    form_class = JobForm
    page_title = 'List of standart jobs'
    nav_link = 'Jobs'
    detail_url = 'shop:job_parts'
    fields = ('name', 'man_hours')
    field_names = ('Description', 'Man-hours')


class JobPartsSetView(WriteCheckMixin, FormSetView):
    model = OrderPart
    form_class = OrderPartForm
    page_title = 'Add parts'
    nav_link = 'Job > Parts'
    template_name = "shop/listview.html"
    redirect_url = './parts'

    def get_object(self):
        return Job.objects.get(id=self.pk)

    def get_queryset(self):
        return self.get_object().parts.all()

    def get_fields(self):
        return {
            'field_names': ['part', 'amount', ],
            'verbose_field_names': ['Part', 'Amount', ],
        }

    def post(self, request, *args, **kwargs):
        formset = self.get_modelformset(request.POST)
        if formset.is_valid():
            job = self.get_object()
            for f in formset:
                inst = f.save(commit=False)
                if inst.amount == 0:
                    inst.delete()
                elif inst.part_id:
                    inst = f.save()
                    job.parts.add(inst)
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))
