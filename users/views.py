from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory

from .models import ListColShow, Profile, PreferenceList, Account, User
from .forms import UserCreationForm, PreferenceListForm, UserLevelForm, BaseUserLevelFormSet
from .utils import generate_profile, not_empty, write_check, admin_check


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


@user_passes_test(admin_check, login_url='users:login')
def users_level_view(request):
    UserFormSet = modelformset_factory(
        Profile,
        form=UserLevelForm,
        fields=['user', 'level',],
        formset=BaseUserLevelFormSet,
        extra=0,
    )
    if request.method != 'POST':
        user_formset = UserFormSet(request=request)
        context = {}
        context['formset'] = user_formset
        return render(request, 'users/update_level.html', context)
    else:
        user_formset = UserFormSet(request.POST, request=request)
        if user_formset.is_valid():
            user_formset.save()
        return redirect(request.user.profile.preferencelist.get_absolute_url())
