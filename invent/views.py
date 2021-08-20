from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Truck, Trailer
from .forms import TruckForm, TrailerForm, BaseTrailerFormSet, BaseTruckFormSet
from .mixins import FormSetView, ReadCheckMixin
from users.utils import gen_field_ver_name, get_columns, read_check, write_check
from users.models import ListColShow


def index(request):
    return render(request, 'invent/index.html')


def permission_denied_view(request, exception):
    message = "You don't have access to this page. Contact your manager."
    return render(request, 'invent/403.html', {'message': message})


class SummaryListView(ReadCheckMixin, ListView):
    model = Truck

    def test_func(self):
        return read_check(self.request.user)

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
            font_class = 'font-small'
        elif font_size == 'L':
            font_class = 'font-large'
        else:
            font_class = 'font-medium'
        context['truck_field_names'] = columns['truck_verbose_field_names']
        context['trailer_field_names'] = columns['trailer_verbose_field_names']
        context['driver_field_names'] = columns['driver_verbose_field_names']
        context['font_class'] = font_class
        context['btn_back'] = True
        context['page_title'] = 'Summary'
        return context


class TruckFormSetView(ReadCheckMixin, FormSetView):
    model = Truck
    form = TruckForm
    formset = BaseTruckFormSet
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:truck'
    redirect_url = 'invent:list_trucks'


class TrailerFormSetView(ReadCheckMixin, FormSetView):
    model = Trailer
    form = TrailerForm
    formset = BaseTrailerFormSet
    page_title = 'List of truck records'
    nav_link = 'Trucks'
    detail_url = 'invent:trailer'
    redirect_url = 'invent:list_trailers'


class TruckDetailView(ReadCheckMixin, DetailView):
    model = Truck


class TrailerDetailView(ReadCheckMixin, DetailView):
    model = Trailer

