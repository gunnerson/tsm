from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from .models import ListColShow, Profile, PreferenceList
from .forms import PreferenceListForm
from .utils import generate_profile


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('users:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Generate default settings
            new_profile = Profile(user=new_user).save()
            generate_profile(request)
            ls = ListColShow.objects.filter(profile=new_profile)
            dls = ListColShow.objects.filter(profile=admin)
            for l in ls:
                d = dls.get(
                    list_name=l.list_name,
                    field_name=l.field_name,
                )
                l.show = d.show
                l.save(update_fields=['show'])
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('invent:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)


class PreferenceListUpdateView(LoginRequiredMixin, UpdateView):
    model = PreferenceList
    form_class = PreferenceListForm


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
        # elif self.request.GET.get('move_up', None) is not None:
        #     pk = int(self.request.GET.get('move_up'))
        #     q = qs.get(id=pk)
        #     q_order = q.order
        #     if q_order != 0:
        #         q.order -= 1
        #         q2 = qs.get(
        #             list_name=q.list_name,
        #             order=q_order-1,
        #             )
        #         q2.order += 1
        #         q.save(update_fields=['order'])
        #         q2.save(update_fields=['order'])
        # elif self.request.GET.get('move_down', None) is not None:
        #     pk = int(self.request.GET.get('move_down'))
        #     q = qs.get(id=pk)
        #     qs2 = qs.filter(list_name=q.list_name)
        #     qs_count = qs2.count()
        #     q_order = q.order
        #     if q_order != (qs_count - 1):
        #         q.order += 1
        #         q2 = qs2.get(order=q_order+1)
        #         q2.order -= 1
        #         q.save(update_fields=['order'])
        #         q2.save(update_fields=['order'])
        return qs
