from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Truck
from .forms import TruckCreateForm, TruckUpdateForm


def index(request):
    return render(request, 'invent/index.html')


class TruckCreateView(LoginRequiredMixin, CreateView):
    model = Truck
    form_class = TruckCreateForm


class TruckListView(ListView):
    model = Truck


class TruckDetailView(DetailView):
    model = Truck


class TruckUpdateView(LoginRequiredMixin, UpdateView):
    model = Truck
    form_class = TruckUpdateForm

