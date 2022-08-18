from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import user_passes_test
from math import sqrt
from django.conf import settings

from .models import Truck, Trailer, Company
from .forms import TruckForm, TrailerForm, CompanyForm
from .mixins import FormSetView, InfoView
from .utils import get_font_classes, model_to_dict
from .gomotive import get_vehicles_locations, get_fault_codes, get_bulk_vehicles_locations, get_update_odometers
from users.mixins import ReadCheckMixin
from users.utils import read_check
from shop.models import OrderJob


@user_passes_test(read_check, login_url='index')
def summary(request):
    # get_update_odometers()
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
    dots = OrderJob.objects.filter(job_id=37)
    for dot in dots:
        try:
            truck = dot.order.truck
            try:
                if truck.last_dot_date is None or dot.order.closed > truck.last_dot_date:
                    truck.last_dot_date = dot.order.closed
                    truck.save(update_fields=['last_dot_date'])
            except TypeError:
                pass
        except AttributeError:
            trailer = dot.order.trailer
            try:
                if trailer.last_dot_date is None or dot.order.closed > trailer.last_dot_date:
                    trailer.last_dot_date = dot.order.closed
                    trailer.save(update_fields=['last_dot_date'])
            except TypeError:
                pass
    # profile = request.user.profile
    # context = {}
    # ours = request.GET.get('ours', None)
    # query = request.GET.get('query', None)
    # our_companies = Company.objects.filter(group__in=('OU', 'LO'))
    # if ours:
    #     if query:
    #         qs = Truck.objects.search(query, 'Truck')
    #         context['query'] = query
    #     else:
    #         qs = Truck.objects.all()
    #     context['ours'] = True
    # else:
    #     if query:
    #         qs = Truck.objects.search(query, 'Truck', our_companies)
    #         context['query'] = query
    #     else:
    #         qs = Truck.objects.filter(owner__in=our_companies)
    # get_summary_context(qs, profile, context)
    # get_font_classes(profile.font_size, context)
    # context['filter_bar'] = True
    ours = Company.objects.filter(id__in=[1, 2])
    trucks = Truck.objects.filter(owner__in=ours, show=True)
    trailers = Trailer.objects.filter(owner__in=ours, show=True)
    context = {}
    get_font_classes(request.user.profile.font_size, context)
    context['trucks'] = trucks
    context['trailers'] = trailers
    return render(request, 'invent/summary.html', context)


class TruckFormSetView(ReadCheckMixin, FormSetView):
    model = Truck
    form_class = TruckForm
    detail_url = 'invent:truck'


class TrailerFormSetView(ReadCheckMixin, FormSetView):
    model = Trailer
    form_class = TrailerForm
    detail_url = 'invent:trailer'


class CompanyFormSetView(ReadCheckMixin, FormSetView):
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
        if inst.kt_id:
            data = get_vehicles_locations(inst.kt_id)
            context['faults'] = get_fault_codes(inst.kt_id)
            try:
                inst.odometer = data['odometer']
                inst.save(update_fields=['odometer'])
                lat = data['lat']
                lon = data['lon']
                shop_lat = 42.0203018
                shop_lon = -88.318316
                context['gmaps_url'] = "https://maps.google.com/?q={0},{1}".format(
                    lat, lon)
                delta_lat = abs(shop_lat - float(lat)) * 111319.9
                delta_lon = abs(shop_lon - float(lon)) * 111319.9
                context['dist_from_shop'] = round(
                    (sqrt(delta_lat**2 + delta_lon**2) * 0.000621371), 1)
                context['desc'] = data['desc']
                context['bearing'] = data['bearing']
                context['driver'] = data['driver']                
            except (IndexError, KeyError):
                pass
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


class MapView(TemplateView):

    template_name = "invent/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = get_bulk_vehicles_locations()
        context['gmaps_api'] = settings.GOOGLE_MAPS_API_KEY
        return context