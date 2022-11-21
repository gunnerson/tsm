from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta, date
from math import sqrt
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponse

from .models import User, ListColShow, Profile, PunchCard, AccountVar
from shop.models import Order, OrderTime, Mechanic, Balance
from .forms import UserCreationForm, ProfileForm, UserLevelForm, PunchCardForm, AccountVarForm
from shop.forms import OrderTimeForm
from .utils import generate_profile
from .mixins import FormSetView, AdminCheckMixin, UserCheckMixin
from .tokens import account_activation_token


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            new_profile = Profile(user=new_user)
            new_profile.save()
            generate_profile(new_profile)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Logistics Pro-Tools account.'
            message = render_to_string('users/activate.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('users:profile', new_profile.id)
    context = {'form': form}
    return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'users/registration_complete.html')
    else:
        return HttpResponse('Activation link is invalid!')


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
            'field_names': ['user', 'level',],
            'verbose_field_names': ['User', 'Access level', ],
        }
        return context

    def get_redirect_url(self):
        return self.request.user.profile.get_absolute_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(Q(user=self.request.user) | Q(level='A'))


@never_cache
def punch(request):
    try:
        profile = request.user.profile
        mechanic = profile.mechanic
        cards = PunchCard.objects.filter(mechanic=mechanic)
        last_card = cards.first()        
        orders = Order.objects.filter(closed=None)
        open_order = None
        open_ordertime = None
        for order in orders:
            ordertimes = order.ordertime_set.all()
            for ordertime in ordertimes:
                if ordertime.start and ordertime.mechanic == mechanic:
                    open_order = order
                    open_ordertime = ordertime
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
            if open_order:
                context['order_select'] = OrderTimeForm(
                    order=open_order,
                    mechanic=mechanic,
                )
                context['stop'] = True
            else:
                context['order_select'] = OrderTimeForm(mechanic=mechanic)
                context['start'] = True
        else:
            selected = request.POST.get('punch_select', None)
            user_lat = request.POST.get('latitude', None)
            user_lon = request.POST.get('longitude', None)
            order_id = request.POST.get('order', None)
            submit = request.POST.get('submit', None)
            status = request.POST.get('status', None)
            order = Order.objects.get(id=order_id) if order_id else open_order
            if user_lat and user_lon:
                shop_lat = float(AccountVar.objects.get(name='SHOP_LAT').value)
                shop_lon = float(AccountVar.objects.get(name='SHOP_LON').value)
                delta_lat = abs(shop_lat - float(user_lat)) * 111319.9
                delta_lon = abs(shop_lon - float(user_lon)) * 111319.9
                distance = round(
                    (sqrt(delta_lat**2 + delta_lon**2) * 0.000621371), 1)
            else:
                distance = 404
            now = timezone.now()            
            if selected == 'punch_in' or (status == 'punched_out'
                                          and submit == 'start'):
                punch_in_standart = now.replace(hour=13, minute=00, second=0)
                if now < punch_in_standart and mechanic.id != 1:
                    punch_in_time = punch_in_standart
                else:
                    punch_in_time = now
                PunchCard(
                    mechanic=mechanic,
                    punch_in=punch_in_time,
                    punch_in_distance=distance,
                ).save()
            elif selected == 'lunch_in':
                if now.date() == last_card.punch_in.date():
                    last_card.lunch_in = now
                else:
                    last_card.lunch_in = last_card.punch_in + timedelta(hours=4)
                last_card.lunch_in_distance = distance
                last_card.save(update_fields=['lunch_in', 'lunch_in_distance'])
                if open_ordertime:
                    open_ordertime.get_total()
            elif selected == 'lunch_out' or (status == 'lunched_in'
                                             and submit == 'start'):
                if now.date() == last_card.punch_in.date():
                    last_card.lunch_out = now
                else:
                    last_card.lunch_out = last_card.punch_in + timedelta(hours=4)
                last_card.lunch_out_distance = distance
                last_card.save(
                    update_fields=['lunch_out', 'lunch_out_distance'])
            elif selected == 'punch_out':
                if now.date() == last_card.punch_in.date():
                    last_card.punch_out = now
                else:
                    last_card.punch_out = last_card.punch_in + timedelta(hours=10)
                last_card.punch_out_distance = distance
                last_card.save(
                    update_fields=['punch_out', 'punch_out_distance'])
                if open_ordertime:
                    open_ordertime.get_total()
            if submit == 'start':
                try:
                    ordertime = order.ordertime_set.get(mechanic=mechanic)
                    ordertime.start = timezone.now()
                    ordertime.save(update_fields=['start'])
                except OrderTime.DoesNotExist:
                    OrderTime(
                        order=order,
                        start=timezone.now(),
                        mechanic=mechanic,
                    ).save()
                if not order.mechanic:
                    order.mechanic = mechanic
                    order.save(update_fields=['mechanic'])
            elif submit == 'stop':
                open_ordertime.get_total()
            return redirect('users:punch')
    except AttributeError:
        context = {}
    return render(request, 'users/punch.html', context)


@method_decorator(never_cache, name='dispatch')
class PunchCardListView(UserCheckMixin, ListView):
    model = PunchCard
    template_name = 'users/punchcards.html'

    def get_queryset(self):
        try:
            mechanic = self.request.GET.get(
                'mechanic', self.request.user.profile.mechanic)
        except ObjectDoesNotExist:
            mechanic = self.request.GET.get(
                'mechanic', None)
        week_of = self.request.GET.get('week_of', None)
        if week_of:
            dt = datetime.strptime(week_of, '%Y-%m-%d')
            if self.request.GET.get('pay_salary', None):
                try:
                    Balance.objects.get(
                        date=dt,
                        category='S',
                        total=-1 *
                        round(float(self.request.GET.get(
                            'salary_amount', None)), 2),
                        comments=Mechanic.objects.get(id=mechanic),
                    )
                except Balance.DoesNotExist:
                    Balance(
                        date=dt,
                        category='S',
                        total=-1 *
                        round(float(self.request.GET.get(
                            'salary_amount', None)), 2),
                        comments=Mechanic.objects.get(id=mechanic),
                    ).save()
        else:
            dt = timezone.now().date()
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=7)
        qs = PunchCard.objects.filter(
            mechanic=mechanic,
            punch_in__range=(start, end),
        ).order_by('punch_in')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_save'] = True
        profile = self.request.user.profile
        mechanic = self.request.GET.get('mechanic', None)
        week_of = self.request.GET.get('week_of', None)
        if week_of:
            week_of = datetime.strptime(week_of, '%Y-%m-%d')
        try:
            selected_mechanic = Mechanic.objects.get(
                id=mechanic) if mechanic else profile.mechanic
        except ObjectDoesNotExist:
            selected_mechanic = None
        context['form'] = PunchCardForm(
            mechanic=selected_mechanic,
            level=profile.level,
            week_of=week_of,
        )
        qs = self.get_queryset()
        week_total = 0
        for q in qs:
            week_total += q.get_hours
        week_total = round(week_total, 1)
        context['week_total'] = week_total
        if selected_mechanic:
            salary = 0
            if week_total <= 50:
                salary = float(selected_mechanic.salary) * week_total
            else:
                salary = float(selected_mechanic.salary) * 50 + \
                    float(selected_mechanic.salary) * 1.5 * (week_total - 50)
            context['salary'] = round(salary, 2)
        if selected_mechanic:
            today = date.today()
            days_employed = today - selected_mechanic.start_date
            context['vacation_days'] = int(
                days_employed.days / 365) * 5 - selected_mechanic.vacation_used
        return context


class AccountVarFormSetView(AdminCheckMixin, FormSetView):
    model = AccountVar
    form_class = AccountVarForm
    extra = 0
    template_name = 'users/account.html'
    page_title = "Update account settings"

    def get_fields(self):
        context = {
            'field_names': ['name', 'value',],
            'verbose_field_names': ['Parameter', 'Value', ],
        }
        return context