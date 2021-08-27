from django.shortcuts import render
from django.views.generic import DetailView
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from .models import Truck, Trailer, Driver, Company
from .forms import TruckForm, TrailerForm, DriverForm, CompanyForm
from .mixins import FormSetView, ReadCheckMixin, WriteCheckMixin
from .utils import get_summary_context


@login_required
def summary(request):
    profile = request.user.profile
    context = {}
    query = request.GET.get('query', None)
    if query:
        qs = Truck.objects.search(query, 'Truck')
        context['query'] = query
    else:
        qs = Truck.objects.all()
    if not request.GET.get('term', None):
        qs = qs.exclude(status='T')
    else:
        context['term'] = True
    get_summary_context(qs, profile, context)
    font_size = profile.font_size
    if font_size == 'S':
        context['font_class'] = 'font-small'
    elif font_size == 'L':
        context['font_class'] = 'font-large'
    else:
        context['font_class'] = 'font-medium'
    context['btn_back'] = True
    context['filter_bar'] = True
    context['page_title'] = 'Summary'
    return render(request, 'invent/summary.html', context)


class TruckFormSetView(WriteCheckMixin, FormSetView):
    model = Truck
    form_class = TruckForm
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:truck'


class TrailerFormSetView(WriteCheckMixin, FormSetView):
    model = Trailer
    form_class = TrailerForm
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:trailer'


class DriverFormSetView(WriteCheckMixin, FormSetView):
    model = Driver
    form_class = DriverForm
    page_title = 'List of driver records'
    nav_link = 'Drivers'
    detail_url = 'invent:driver'


class CompanyFormSetView(WriteCheckMixin, FormSetView):
    model = Company
    form_class = CompanyForm
    page_title = 'List of company records'
    nav_link = 'Companies'
    detail_url = 'invent:company'


class TruckDetailView(ReadCheckMixin, DetailView):
    model = Truck


class TrailerDetailView(ReadCheckMixin, DetailView):
    model = Trailer

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['page_title'] = 'Trailer info'
        context['nav_link'] = 'Trailer'
        return context


class DriverDetailView(ReadCheckMixin, DetailView):
    model = Driver

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['page_title'] = 'Driver info'
        context['nav_link'] = 'Driver'
        return context


class CompanyDetailView(ReadCheckMixin, DetailView):
    model = Company

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['page_title'] = 'Company info'
        context['nav_link'] = 'Company'
        return context
