from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
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
            authenticated_user = authenticate(email=new_user.email,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return redirect('users:preferences', new_preflist.id)
    return render(request, 'users/register.html', {'form': form})


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
        return context


class ListColShowListView(LoginRequiredMixin, ListView):
    model = ListColShow

    def get_queryset(self):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
        if self.request.GET.get('changed', None):
            for q in qs:
                checked = self.request.GET.get(str(q.id), None)
                if checked:
                    q.show = True
                else:
                    q.show = False
                q.save(update_fields=['show'])
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_back'] = True
        context['btn_save'] = True
        context['btn_custom'] = True
        context['page_title'] = ''
        return context


class UsersLevelFormSetView(UserPassesTestMixin, FormSetView):
    model = Profile
    form = UserLevelForm
    extra = 0
    btn_custom = True
    page_title = "Update users' privileges"
    nav_link = 'Privileges'
    set_redirect = True

    def test_func(self):
        return admin_check(self.request.user)

    def get_fields(self):
        context = {'field_names': ['user', 'level', ]}
        return context

    def get_redirect_url(self):
        return self.request.user.profile.preferencelist.get_absolute_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(~Q(user=self.request.user))
