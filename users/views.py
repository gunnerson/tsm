from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from django.db.models import Q

from .models import ListColShow, Profile, PreferenceList, Account
from .forms import UserCreationForm, PreferenceListForm, UserLevelForm
from .utils import generate_profile, not_empty, admin_check
from invent.mixins import FormSetView


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_account_name = request.POST['new_account']
            if not_empty(new_account_name):
                new_account = Account(name=new_account_name)
                new_account.save()
                new_user.account = new_account
                new_user.save()
                new_profile = Profile(
                    user=new_user,
                    account=new_account,
                    level='A',
                )
                new_profile.save()
            else:
                new_user.save()
                account = Account.objects.get(id=request.POST['account'])
                new_profile = Profile(user=new_user, account=account)
                new_profile.save()
            generate_profile(new_profile)
            new_preflist = PreferenceList(profile=new_profile)
            new_preflist.save()
            authenticated_user = authenticate(
                email=new_user.email,
                password=request.POST['password1'],
            )
            login(request, authenticated_user)
            return redirect('users:preferences', new_preflist.id)
    context = {
        'form': form,
        'btn_back': True,
        'page_title': 'Register new user account',
        'nav_link': 'Register',
    }
    return render(request, 'users/register.html', context)


class UserLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login to your account'
        context['btn_back'] = True
        context['nav_link'] = 'Login'
        return context


class PreferenceListUpdateView(LoginRequiredMixin, UpdateView):
    model = PreferenceList
    form_class = PreferenceListForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        user = self.object.profile.user
        user.first_name = first_name
        user.last_name = last_name
        user.save(update_fields=['first_name', 'last_name'])
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        context['btn_custom'] = True
        context['page_title'] = 'Account settings'
        context['nav_link'] = 'Preferences'
        context['write_check'] = True
        return context


class ListColShowListView(LoginRequiredMixin, ListView):
    model = ListColShow

    def get_queryset(self):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
        return qs

    def post(self, *args, **kwargs):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
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
        context['btn_back'] = True
        context['btn_save'] = True
        context['btn_custom'] = True
        context['page_title'] = 'Select summary columns'
        context['nav_link'] = 'Columns'
        context['write_check'] = True
        return context


class UsersLevelFormSetView(UserPassesTestMixin, FormSetView):
    model = Profile
    form_class = UserLevelForm
    extra = 0
    btn_custom = True
    page_title = "Update users' privileges"
    nav_link = 'Privileges'

    def test_func(self):
        return admin_check(self.request.user)

    def get_fields(self):
        context = {
            'field_names': ['user', 'level', ],
            'verbose_field_names': ['User', 'Access level', ],
        }
        return context

    def get_redirect_url(self):
        return self.request.user.profile.preferencelist.get_absolute_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(~Q(user=self.request.user))
