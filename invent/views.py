from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Truck, Trailer
from .forms import TruckForm, TrailerForm
from .utils import has_group


def index(request):
    return render(request, 'invent/index.html')


class TruckCreateView(UserPassesTestMixin, CreateView):
    model = Truck
    form_class = TruckForm

    def test_func(self):
        return (has_group(self.request.user, 'writer'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.year_made == '':
            self.object.year_made = None
        self.object.save()
        return redirect(self.object.get_absolute_url())


class TruckListView(UserPassesTestMixin, ListView):
    model = Truck

    def test_func(self):
        return (has_group(self.request.user, 'viewer'))


class TruckUpdateView(UserPassesTestMixin, UpdateView):
    model = Truck
    form_class = TruckForm
    template_name_suffix = '_update'

    def test_func(self):
        return (has_group(self.request.user, 'writer'))

    def get_initial(self):
        initial = super(TruckUpdateView, self).get_initial()
        try:
            initial['driver'] = self.object.driver
        except Truck.driver.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Re-assign to another driver
        driver = form.cleaned_data['driver']
        if driver is not None:
            driver.truck = self.object
            driver.save(update_fields=['truck'])
        if self.object.year_made == '':
            self.object.year_made = None
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=True)
        return kwargs


class TrailerCreateView(UserPassesTestMixin, CreateView):
    model = Trailer
    form_class = TrailerForm

    def test_func(self):
        return (has_group(self.request.user, 'writer'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.year_made == '':
            self.object.year_made = None
        self.object.save()
        return redirect(self.object.get_absolute_url())


class TrailerListView(UserPassesTestMixin, ListView):
    model = Trailer

    def test_func(self):
        return (has_group(self.request.user, 'viewer'))


class TrailerUpdateView(UserPassesTestMixin, UpdateView):
    model = Trailer
    form_class = TrailerForm
    template_name_suffix = '_update'

    def test_func(self):
        return (has_group(self.request.user, 'writer'))

    def get_initial(self):
        initial = super(TrailerUpdateView, self).get_initial()
        try:
            initial['driver'] = self.object.driver
        except Trailer.driver.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Re-assign to another driver
        driver = form.cleaned_data['driver']
        if driver is not None:
            driver.trailer = self.object
            driver.save(update_fields=['trailer'])
        if self.object.year_made == '':
            self.object.year_made = None
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=True)
        return kwargs
