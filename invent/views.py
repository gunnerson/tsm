from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Truck, Trailer
from .forms import TruckForm, TrailerForm


def index(request):
    return render(request, 'invent/index.html')


class TruckCreateView(LoginRequiredMixin, CreateView):
    model = Truck
    form_class = TruckForm


class TruckListView(LoginRequiredMixin, ListView):
    model = Truck


class TruckUpdateView(LoginRequiredMixin, UpdateView):
    model = Truck
    form_class = TruckForm
    template_name_suffix = '_update'


class TrailerCreateView(LoginRequiredMixin, CreateView):
    model = Trailer
    form_class = TrailerForm


class TrailerListView(LoginRequiredMixin, ListView):
    model = Trailer


class TrailerUpdateView(LoginRequiredMixin, UpdateView):
    model = Trailer
    form_class = TrailerForm
    template_name_suffix = '_update'
