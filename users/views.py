from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from math import sqrt

from .models import ListColShow, Profile, PunchCard
from shop.models import Order, OrderTime
from .forms import UserCreationForm, ProfileForm, UserLevelForm, PunchCardForm
from shop.forms import OrderTimeForm
from .utils import generate_profile
from .mixins import FormSetView, AdminCheckMixin


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profile(user=new_user)
            new_profile.save()
            generate_profile(new_profile)
            authenticated_user = authenticate(
                email=new_user.email,
                password=request.POST['password1'],
            )
            login(request, authenticated_user)
            return redirect('users:profile', new_profile.id)
    context = {'form': form}
    return render(request, 'users/register.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        self.object = form.save()
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        user = self.object.user
        user.first_name = first_name
        user.last_name = last_name
        user.save(update_fields=['first_name', 'last_name'])
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        return context


class ListColShowListView(LoginRequiredMixin, ListView):
    model = ListColShow

    def get_queryset(self):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
        return qs

    def post(self, *args, **kwargs):
        qs = self.get_queryset()
        if self.request.POST.get('check_all', None):
            for q in qs:
                q.show = True
                q.save(update_fields=['show'])
        elif self.request.POST.get('uncheck_all', None):
            for q in qs:
                if q.field_name not in ('truck', 'trailer'):
                    q.show = False
                    q.save(update_fields=['show'])
        else:
            for q in qs:
                if q.field_name not in ('truck', 'trailer'):
                    checked = self.request.POST.get(str(q.id), None)
                    if checked:
                        q.show = True
                    else:
                        q.show = False
                    q.save(update_fields=['show'])
        if self.request.POST.get('move_up', None):
            q_id = self.request.POST.get('move_up')
            q = qs.get(id=q_id)
            if q.order > 1:
                q.order -= 1
                prev_q = qs.get(list_name=q.list_name, order=q.order)
                q.save(update_fields=['order'])
                prev_q.order += 1
                prev_q.save(update_fields=['order'])
        elif self.request.POST.get('move_down', None):
            q_id = self.request.POST.get('move_down')
            q = qs.get(id=q_id)
            if q.order < qs.filter(list_name=q.list_name).count():
                q.order += 1
                next_q = qs.get(list_name=q.list_name, order=q.order)
                q.save(update_fields=['order'])
                next_q.order -= 1
                next_q.save(update_fields=['order'])
        return redirect('users:listcolshow')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        return context


class UsersLevelFormSetView(AdminCheckMixin, FormSetView):
    model = Profile
    form_class = UserLevelForm
    extra = 0
    page_title = "Update users' privileges"
    nav_link = 'Privileges'
    filter_bar = False
    template_name = 'users/listview.html'

    def get_fields(self):
        context = {
            'field_names': ['user', 'level', 'home_latitude', 'home_longitude'],
            'verbose_field_names': ['User', 'Access level', 'Latitude', 'Longitude'],
        }
        return context

    def get_redirect_url(self):
        return self.request.user.profile.get_absolute_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(Q(user=self.request.user) | Q(level='A'))


def punch(request):
    profile = request.user.profile
    mechanic = profile.mechanic
    cards = PunchCard.objects.filter(mechanic=mechanic)
    last_card = cards.last()
    if request.method != 'POST':
        context = {}
        no_card = True
        status = 'punched_out'
        if last_card:
            no_card = False
            if last_card.punch_in:
                status = 'punched_in'
            if last_card.lunch_in:
                status = 'lunched_in'
            if last_card.lunch_out:
                status = 'lunched_out'
            if last_card.punch_out:
                status = 'punched_out'
        context['status'] = status
        context['no_card'] = no_card
        orders = mechanic.order_set.filter(closed=None)
        for inst in orders:
            last_ordertime = inst.ordertime_set.last()
            if last_ordertime and not last_ordertime.stop:
                open_order = last_ordertime.order
            else:
                open_order = None
        if open_order:
            context['order_select'] = OrderTimeForm(
                order=last_ordertime.order)
            context['stop'] = True
        else:
            context['order_select'] = OrderTimeForm()
            context['start'] = True
    else:
        selected = request.POST.get('punch_select', None)
        user_lat = request.POST.get('latitude', None)
        user_lon = request.POST.get('longitude', None)
        if user_lat and user_lon:
            shop_lat = profile.home_latitude
            shop_lon = profile.home_longitude
            delta_lat = abs(shop_lat - float(user_lat)) * 111319.9
            delta_lon = abs(shop_lon - float(user_lon)) * 111319.9
            distance = round(
                (sqrt(delta_lat**2 + delta_lon**2) * 0.000621371), 1)
        else:
            distance = 404
        if selected == 'punch_in':
            PunchCard(
                mechanic=mechanic,
                punch_in=timezone.now(),
                punch_in_distance=distance,
            ).save()
        elif selected == 'lunch_in':
            last_card.lunch_in = timezone.now()
            last_card.lunch_in_distance = distance
            last_card.save(update_fields=['lunch_in', 'lunch_in_distance'])
        elif selected == 'lunch_out':
            last_card.lunch_out = timezone.now()
            last_card.lunch_out_distance = distance
            last_card.save(update_fields=['lunch_out', 'lunch_out_distance'])
        elif selected == 'punch_out':
            last_card.punch_out = timezone.now()
            last_card.punch_out_distance = distance
            last_card.save(update_fields=['punch_out', 'punch_out_distance'])
        order_id = request.POST.get('order', None)
        if order_id:
            order = Order.objects.get(id=order_id)
        submit = request.POST.get('submit', None)
        if submit == 'start':
            OrderTime(order=order, start=timezone.now()).save()
            order.mechanic = mechanic
            order.save(update_fields=['mechanic'])
        elif submit == 'stop':
            ordertime = order.ordertime_set.last()
            ordertime.stop = timezone.now()
            ordertime.save(update_fields=['stop'])
        return redirect('users:punch')
    return render(request, 'users/punch.html', context)


class PunchCardListView(LoginRequiredMixin, ListView):
    model = PunchCard
    template_name = 'users/punchcards.html'

    def get_queryset(self):
        mechanic = self.request.GET.get('mechanic', None)
        week_of = self.request.GET.get('week_of', None)
        if mechanic and week_of:
            dt = datetime.strptime(week_of, '%Y-%m-%d')
            start = dt - timedelta(days=dt.weekday())
            end = start + timedelta(days=7)
            qs = PunchCard.objects.filter(
                mechanic=mechanic,
                punch_in__range=(start, end),
            )
        else:
            qs = PunchCard.objects.filter(
                mechanic=self.request.user.profile.mechanic)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        profile = self.request.user.profile
        mechanic = self.request.GET.get('mechanic', None)
        week_of = self.request.GET.get('week_of', None)
        if week_of:
            week_of = datetime.strptime(week_of, '%Y-%m-%d')
        new_mechanic = mechanic if mechanic else profile.mechanic
        context['form'] = PunchCardForm(
            mechanic=new_mechanic,
            level=profile.level,
            week_of=week_of,
        )
        qs = self.get_queryset()
        week_total = 0
        for q in qs:
            week_total += q.get_hours
        context['week_total'] = week_total
        return context
