from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from .models import ListColShow, Profile, PreferenceList
from .forms import UserCreationForm, PreferenceListForm
from .utils import generate_profile


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
            new_preflist = PreferenceList(profile=new_profile)
            new_preflist.save()
            authenticated_user = authenticate(email=new_user.email,
                                              password=request.POST['password2'])
            login(request, authenticated_user)
            return redirect('users:preferences', new_preflist.id)
    return render(request, 'users/register.html', {'form': form})


class PreferenceListUpdateView(LoginRequiredMixin, UpdateView):
    model = PreferenceList
    form_class = PreferenceListForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['email'] = user.email
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial


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
