from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import modelformset_factory

from invent.mixins import WriteCheckMixin

from .models import Order
from .forms import OrderForm


class OrderCreateView(WriteCheckMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
