from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Driver, Company, PasswordGroup
from .forms import DriverForm, CompanyForm, PasswordGroupForm
from invent.models import Truck, Trailer
from users.utils import read_check, write_check


class DriverCreateView(UserPassesTestMixin, CreateView):
    model = Driver
    form_class = DriverForm

    def test_func(self):
        return write_check(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.request.user.profile.account
        self.object.save()
        return redirect(self.object.get_absolute_url())

class DriverListView(UserPassesTestMixin, ListView):
    model = Driver

    def test_func(self):
        return read_check(self.request.user)


class DriverUpdateView(UserPassesTestMixin, UpdateView):
    model = Driver
    form_class = DriverForm
    template_name_suffix = '_update'

    def test_func(self):
        return write_check(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=True)
        return kwargs

    def get_initial(self):
        initial = super(DriverUpdateView, self).get_initial()
        initial['truck'] = self.object.truck
        initial['trailer'] = self.object.trailer
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Re-assign truck relationship
        truck = form.cleaned_data['truck']
        if truck is not None:
            try:
                old_driver = truck.driver
                old_driver.truck = None
                old_driver.save(update_fields=['truck'])
            except Truck.driver.RelatedObjectDoesNotExist:
                pass
            self.object.truck = truck
        # Re-assign trailer relationship
        trailer = form.cleaned_data['trailer']
        if trailer is not None:
            try:
                old_driver = trailer.driver
                old_driver.trailer = None
                old_driver.save(update_fields=['trailer'])
            except Trailer.driver.RelatedObjectDoesNotExist:
                pass
            self.object.trailer = trailer
        self.object.save()
        return redirect(self.object.get_absolute_url())


class CompanyCreateView(UserPassesTestMixin, CreateView):
    model = Company
    form_class = CompanyForm

    def test_func(self):
        return write_check(self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.request.user.profile.account
        self.object.save()
        return redirect(self.object.get_absolute_url())


class CompanyListView(UserPassesTestMixin, ListView):
    model = Company

    def test_func(self):
        return read_check(self.request.user)


class CompanyUpdateView(UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name_suffix = '_update'

    def test_func(self):
        return write_check(self.request.user)


class PasswordGroupCreateView(UserPassesTestMixin, CreateView):
    model = PasswordGroup
    form_class = PasswordGroupForm

    def test_func(self):
        return write_check(self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.request.user.profile.account
        self.object.save()
        return redirect(self.object.get_absolute_url())
