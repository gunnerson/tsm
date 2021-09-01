from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import Truck, Trailer, Driver, Company
from .forms import TruckForm, TrailerForm, DriverForm, CompanyForm
from .mixins import FormSetView
from users.mixins import ReadCheckMixin, WriteCheckMixin
from .utils import get_summary_context, get_font_classes


@login_required
def summary(request):
    profile = request.user.profile
    context = {}
    ours = request.GET.get('ours', None)
    query = request.GET.get('query', None)
    our_companies = Company.objects.filter(group='OU')
    if ours:
        if query:
            qs = Truck.objects.search(query, 'Truck')
            context['query'] = query
        else:
            qs = Truck.objects.all()
        context['ours'] = True
    else:
        if query:
            qs = Truck.objects.search(query, 'Truck', our_companies)
            context['query'] = query
        else:
            qs = Truck.objects.filter(owner__in=our_companies)
    if not request.GET.get('term', None):
        qs = qs.exclude(status='T')
    else:
        context['term'] = True
    get_summary_context(qs, profile, context)
    get_font_classes(profile.font_size, context)
    context['filter_bar'] = True
    return render(request, 'invent/summary.html', context)


class TruckFormSetView(WriteCheckMixin, FormSetView):
    model = Truck
    form_class = TruckForm
    detail_url = 'invent:truck'


class TrailerFormSetView(WriteCheckMixin, FormSetView):
    model = Trailer
    form_class = TrailerForm
    detail_url = 'invent:trailer'


class DriverFormSetView(WriteCheckMixin, FormSetView):
    model = Driver
    form_class = DriverForm
    detail_url = 'invent:driver'


class CompanyFormSetView(WriteCheckMixin, FormSetView):
    model = Company
    form_class = CompanyForm
    detail_url = 'invent:company'


class TruckDetailView(ReadCheckMixin, DetailView):
    model = Truck


class TrailerDetailView(ReadCheckMixin, DetailView):
    model = Trailer


class DriverDetailView(ReadCheckMixin, DetailView):
    model = Driver


class CompanyDetailView(ReadCheckMixin, DetailView):
    model = Company
