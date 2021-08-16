from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Truck, Trailer
from .forms import TruckForm, TrailerForm
from users.utils import has_access, not_empty, gen_field_ver_name
from users.models import ListColShow


def index(request):
    return render(request, 'invent/index.html')


class TruckCreateView(UserPassesTestMixin, CreateView):
    model = Truck
    form_class = TruckForm

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.year == '':
            self.object.year = None
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


class TruckListView(UserPassesTestMixin, ListView):
    model = Truck

    def test_func(self):
        return has_access(self.request.user, 'read')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = ListColShow.objects.filter(
            profile=self.request.user.profile,
            list_name=str(self.model._meta.verbose_name).capitalize(),
        )
        field_names = []
        for q in qs:
            if q.show:
                field_names.append(q.field_name)
        font_size = self.request.user.profile.preferencelist.trucks_font
        if font_size == 'S':
            font_class = 'font-small'
        elif font_size == 'L':
            font_class = 'font-large'
        else:
            font_class = 'font-medium'
        context['field_names'] = field_names
        context['font_class'] = font_class
        return context


class TruckUpdateView(UserPassesTestMixin, UpdateView):
    model = Truck
    form_class = TruckForm
    template_name_suffix = '_update'

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_initial(self):
        initial = super(TruckUpdateView, self).get_initial()
        try:
            initial['driver'] = self.object.driver
        except Truck.driver.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Re-assign to another driver
        driver = form.cleaned_data['driver']
        if driver is not None:
            driver.truck = self.object
            driver.save(update_fields=['truck'])
        if self.object.year == '':
            self.object.year = None
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=True)
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
        kwargs.update(is_update=False)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.year_made == '':
            self.object.year_made = None
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


class TrailerListView(UserPassesTestMixin, ListView):
    model = Trailer

    def test_func(self):
        return has_access(self.request.user, 'read')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        col_count = 6
        table_style = 'grid-template-columns: repeat(' + \
            str(col_count) + ', 1fr)'
        context['table_style'] = table_style
        return context


class TrailerUpdateView(UserPassesTestMixin, UpdateView):
    model = Trailer
    form_class = TrailerForm
    template_name_suffix = '_update'

    def test_func(self):
        return has_access(self.request.user, 'write')

    def get_initial(self):
        initial = super(TrailerUpdateView, self).get_initial()
        try:
            initial['driver'] = self.object.driver
        except Trailer.driver.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Re-assign to another driver
        driver = form.cleaned_data['driver']
        if driver is not None:
            driver.trailer = self.object
            driver.save(update_fields=['trailer'])
        if self.object.year_made == '':
            self.object.year_made = None
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(is_update=True)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['upper_name'] = "Trailer"
        context['lower_name'] = "trailer"
        context['url_left_1_a'] = "invent:list_trailers"
        context['url_left_1_t'] = "Back"
        return context
