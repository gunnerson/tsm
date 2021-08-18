from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import modelformset_factory

from .models import Truck, Trailer
from .forms import TruckForm, TrailerForm, BaseTrailerFormSet, BaseTruckFormSet
from users.utils import (has_access, not_empty, gen_field_ver_name,
                         get_columns, read_check, write_check)
from users.models import ListColShow


def index(request):
    return render(request, 'invent/index.html')


class SummaryListView(UserPassesTestMixin, ListView):
    model = Truck

    def test_func(self):
        return has_access(self.request.user, 'read')

    def get_queryset(self):
        account = self.request.user.profile.account
        query = self.request.GET.get('query', None)
        if not_empty(query):
            qs = Truck.objects.search(query, account)
        else:
            qs = Truck.objects.filter(account=account)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        columns = get_columns(self.request.user)
        font_size = self.request.user.profile.preferencelist.trucks_font
        if font_size == 'S':
            font_class = 'font-small'
        elif font_size == 'L':
            font_class = 'font-large'
        else:
            font_class = 'font-medium'
        context['truck_field_names'] = columns['truck_verbose_field_names']
        context['trailer_field_names'] = columns['trailer_verbose_field_names']
        context['driver_field_names'] = columns['driver_verbose_field_names']
        context['font_class'] = font_class
        return context


class TruckCreateView(UserPassesTestMixin, CreateView):
    model = Truck
    form_class = TruckForm

    def test_func(self):
        return has_access(self.request.user, 'write')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.request.user.profile.account
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['upper_name'] = "Truck"
        context['lower_name'] = "truck"
        context['url_left_1_a'] = "invent:list_trucks"
        context['url_left_1_t'] = "Back"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_view=True)
        return kwargs

@user_passes_test(write_check,
                  login_url='invent:index',
                  redirect_field_name=None)
def trucks_list_view(request):
    columns = get_columns(request.user)
    TruckFormSet = modelformset_factory(
        Truck,
        form=TruckForm,
        fields=columns['truck_field_names'],
        formset=BaseTruckFormSet,
    )
    if request.method != 'POST':
        truck_formset = TruckFormSet(request=request)
        context = {}
        font_size = request.user.profile.preferencelist.trucks_font
        context['fields'] = columns['truck_verbose_field_names']
        context['formset'] = truck_formset
        return render(request, 'invent/truck_list.html', context)
    else:
        truck_formset = TruckFormSet(request.POST, request=request)
        if truck_formset.is_valid():
            instances = truck_formset.save(commit=False)
            for i in instances:
                i.account = request.user.profile.account
                i.save()
        return redirect('invent:list_trucks')


class TruckUpdateView(UserPassesTestMixin, UpdateView):
    model = Truck
    form_class = TruckForm

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_view=True)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['upper_name'] = "Truck"
        context['lower_name'] = "truck"
        context['url_left_1_a'] = "invent:list_trucks"
        context['url_left_1_t'] = "Back"
        return context


class TrailerCreateView(UserPassesTestMixin, CreateView):
    model = Trailer
    form_class = TrailerForm

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_view=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.request.user.profile.account
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['upper_name'] = "Trailer"
        context['lower_name'] = "trailer"
        context['url_left_1_a'] = "invent:list_trailers"
        context['url_left_1_t'] = "Back"
        return context


@user_passes_test(write_check,
                  login_url='invent:index',
                  redirect_field_name=None)
def trailers_list_view(request):
    columns = get_columns(request.user)
    TrailerFormSet = modelformset_factory(
        Trailer,
        form=TrailerForm,
        fields=columns['trailer_field_names'],
        formset=BaseTrailerFormSet,
    )
    if request.method != 'POST':
        trailer_formset = TrailerFormSet(request=request)
        context = {}
        context['fields'] = columns['trailer_verbose_field_names']
        context['formset'] = trailer_formset
        return render(request, 'invent/trailer_list.html', context)
    else:
        trailer_formset = TrailerFormSet(request.POST, request=request)
        if trailer_formset.is_valid():
            instances = trailer_formset.save(commit=False)
            for i in instances:
                i.account = request.user.profile.account
                i.save()
        return redirect('invent:list_trailers')


class TrailerUpdateView(UserPassesTestMixin, UpdateView):
    model = Trailer
    form_class = TrailerForm

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_view=True)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['upper_name'] = "Trailer"
        context['lower_name'] = "trailer"
        context['url_left_1_a'] = "invent:list_trailers"
        context['url_left_1_t'] = "Back"
        return context
