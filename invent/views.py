from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Truck, Trailer, Driver
from .forms import TruckForm, TrailerForm, DriverForm
from .mixins import FormSetView, ReadCheckMixin
from users.utils import get_columns


def index(request):
    return render(request, 'invent/index.html')


def permission_denied_view(request, exception):
    message = "You don't have access to this page. Contact account administrator."
    return render(request, 'invent/403.html', {'message': message})


class SummaryListView(ReadCheckMixin, ListView):
    model = Truck

    def get_queryset(self):
        account = self.request.user.profile.account
        query = self.request.GET.get('query', None)
        if query:
            qs = Truck.objects.search(query, account)
        else:
            qs = Truck.objects.filter(account=account)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        columns = get_columns(self.request.user)
        font_size = self.request.user.profile.preferencelist.font_size
        if font_size == 'S':
            context['font_class'] = 'font-small'
        elif font_size == 'L':
            context['font_class'] = 'font-large'
        else:
            context['font_class'] = 'font-medium'
        context['truck_field_names'] = columns['truck_verbose_field_names']
        context['trailer_field_names'] = columns['trailer_verbose_field_names']
        context['driver_field_names'] = columns['driver_verbose_field_names']
        context['btn_back'] = True
        context['page_title'] = 'Summary'
        return context


class TruckFormSetView(ReadCheckMixin, FormSetView):
    model = Truck
    form = TruckForm
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:truck'


class TrailerFormSetView(ReadCheckMixin, FormSetView):
    model = Trailer
    form = TrailerForm
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:trailer'


class DriverFormSetView(ReadCheckMixin, FormSetView):
    model = Driver
    form = DriverForm
    page_title = 'List of driver records'
    nav_link = 'Drivers'
    detail_url = 'invent:driver'


class TruckDetailView(ReadCheckMixin, DetailView):
    model = Truck


class TrailerDetailView(ReadCheckMixin, DetailView):
    model = Trailer


class DriverDetailView(ReadCheckMixin, DetailView):
    model = Driver
