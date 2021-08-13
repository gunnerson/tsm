from django.shortcuts import render, redirect
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

    def get_initial(self):
        initial = super(TruckUpdateView, self).get_initial()
        try:
            initial['driver'] = self.object.driver
        except Truck.driver.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        driver = form.cleaned_data['driver']
        driver.truck = self.object
        driver.save(update_fields=['truck'])
        self.object.save()
        return redirect(self.object.get_absolute_url())



class TrailerCreateView(LoginRequiredMixin, CreateView):
    model = Trailer
    form_class = TrailerForm


class TrailerListView(LoginRequiredMixin, ListView):
    model = Trailer


class TrailerUpdateView(LoginRequiredMixin, UpdateView):
    model = Trailer
    form_class = TrailerForm
    template_name_suffix = '_update'
