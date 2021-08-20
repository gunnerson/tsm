from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import modelformset_factory


from .models import Driver, Company, PasswordGroup
from .forms import DriverForm, BaseDriverFormSet, CompanyForm, \
    PasswordGroupForm
from invent.models import Truck, Trailer
from users.utils import get_columns, read_check, write_check


@user_passes_test(read_check, login_url='invent:index')
def drivers_list_view(request):
    columns = get_columns(request.user)
    DriverFormSet = modelformset_factory(
        Driver,
        form=DriverForm,
        fields=columns['driver_field_names'],
        formset=BaseDriverFormSet,
    )
    context = {'fields': columns['driver_verbose_field_names']}
    context['write_check'] = write_check(request.user)
    if request.method != 'POST':
        driver_formset = DriverFormSet(request=request)
    else:
        driver_formset = DriverFormSet(request.POST, request=request)
        if driver_formset.is_valid():
            instances = driver_formset.save(commit=False)
            for i in instances:
                i.account = request.user.profile.account
                i.save()
            return redirect('contacts:list_drivers')
    context['formset'] = driver_formset
    return render(request, 'contacts/driver_list.html', context)


class DriverCreateView(UserPassesTestMixin, CreateView):
    model = Driver
    form_class = DriverForm

    def test_func(self):
        return write_check(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_view=True)
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
        kwargs.update(is_view=True)
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
