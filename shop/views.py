from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import modelformset_factory

from invent.mixins import ReadCheckMixin, WriteCheckMixin

from .models import Order
from .forms import OrderForm


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


class OrderDetailView(ReadCheckMixin, DetailView):
    model = Order
    template_name = 'shop/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['page_title'] = 'Order #' + str(self.get_object().id)
        context['nav_link'] = 'Order'
        return context


class OrderUpdateView(WriteCheckMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/form.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        context['page_title'] = 'Update order #' + self.get_object().__str__()
        context['nav_link'] = 'Update order'
        return context
