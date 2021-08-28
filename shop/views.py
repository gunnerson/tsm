from django.shortcuts import render, redirect
# from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from invent.mixins import ReadCheckMixin, WriteCheckMixin

from .models import Order
from .forms import OrderForm
from .utils import get_job_forms
from .mixins import ObjectView


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


class OrderCreateView(WriteCheckMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_create=True)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        context['page_title'] = 'Create new work order'
        context['nav_link'] = 'New order'
        return context


class OrderUpdateView(WriteCheckMixin, ObjectView):
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
                    if inst.job_id:
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
