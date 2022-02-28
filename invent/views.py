from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test

from .models import Truck, Trailer, Company
from .forms import TruckForm, TrailerForm, CompanyForm
from .mixins import FormSetView, InfoView
from .utils import get_summary_context, get_font_classes, model_to_dict
from users.mixins import ReadCheckMixin, WriteCheckMixin
from users.utils import read_check
from shop.models import OrderJob


@user_passes_test(read_check, login_url='index')
def summary(request):
    pms = OrderJob.objects.filter(job_id=22)
    for pm in pms:
        truck = pm.order.truck
        try:
            if truck.last_pm_date is None or truck.last_pm_mls is None or pm.order.closed > truck.last_pm_date:
                truck.last_pm_date = pm.order.closed
                truck.last_pm_mls = pm.order.mileage
                truck.save(update_fields=['last_pm_date', 'last_pm_mls'])
        except TypeError:
            pass
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
        context['order_list'] = inst.order_set.all()
        context['part_list'] = inst.part_set.all()
        context['assigned_parts_list'] = inst.partplace_set.all()
        context['btn_assign_truck'] = True
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
        context['order_list'] = inst.order_set.all()
        context['part_list'] = inst.part_set.all()
        context['assigned_parts_list'] = inst.partplace_set.all()
        context['btn_assign_trailer'] = True
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
