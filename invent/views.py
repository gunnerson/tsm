from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test

from .models import Truck, Trailer, Driver, Company
from .forms import TruckForm, TrailerForm, DriverForm, CompanyForm
from .mixins import FormSetView, InfoView
from .utils import get_summary_context, get_font_classes, model_to_dict
from users.mixins import ReadCheckMixin, WriteCheckMixin
from users.utils import read_check


@user_passes_test(read_check, login_url='index')
def summary(request):
    profile = request.user.profile
    context = {}
    ours = request.GET.get('ours', None)
    query = request.GET.get('query', None)
    our_companies = Company.objects.filter(group__in=('OU', 'LO'))
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


class TruckDetailView(ReadCheckMixin, InfoView):
    model = Truck
    image_url = 'docs:truck_image'
    gallery_url = 'docs:truck_images'
    doc_url = 'docs:truck_doc'
    files_url = 'docs:truck_files'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        inst = self.get_object()
        context['last_inspection'] = inst.truck_pms.last()
        context['order_list'] = inst.order_set.all()
        return context


class TrailerDetailView(ReadCheckMixin, InfoView):
    model = Trailer
    image_url = 'docs:trailer_image'
    gallery_url = 'docs:trailer_images'
    doc_url = 'docs:trailer_doc'
    files_url = 'docs:trailer_files'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        inst = self.get_object()
        context['last_inspection'] = inst.trailer_pms.last()
        context['order_list'] = inst.order_set.all()
        return context


class DriverDetailView(ReadCheckMixin, DetailView):
    model = Driver

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        inst = self.get_object()
        context['fields'] = model_to_dict(inst, exclude=('id'))
        context['inst_id'] = inst.id
        context['btn_doc'] = True
        context['doc_url'] = 'docs:driver_doc'
        context['btn_files'] = True
        context['files_url'] = 'docs:driver_files'
        return context


class CompanyDetailView(ReadCheckMixin, DetailView):
    model = Company

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        inst = self.get_object()
        context['fields'] = model_to_dict(inst, exclude=('id'))
        context['inst_id'] = inst.id
        context['btn_doc'] = True
        context['doc_url'] = 'docs:company_doc'
        context['btn_files'] = True
        context['files_url'] = 'docs:company_files'
        return context
