from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.forms import modelformset_factory, BaseModelFormSet
from django.contrib.auth.mixins import UserPassesTestMixin

from users.utils import gen_field_ver_name, read_check, write_check
from users.models import ListColShow


class ReadCheckMixin(UserPassesTestMixin):

    def test_func(self):
        return read_check(self.request.user)


class FormSetView():
    model = None
    form = None
    formset = BaseModelFormSet
    btn_back = True
    btn_save = True
    btn_custom = False
    page_title = 'List of records'
    nav_link = 'List'
    detail_url = ''
    template_name = 'invent/listview.html'
    redirect_url = ''
    extra = 1
    set_redirect = False  # specify get_redirect_url() method

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, *args, **kwargs)
        return view

    def dispatch(self, request, *args, **kwargs):
        allowed_methods = ["GET", "POST"]
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        method = getattr(self, self.request.method.lower())
        return method(request, *args, **kwargs)

    def __init__(self, request):
        self.request = request

    def get_fields(self):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
        field_names = []
        verbose_field_names = []
        for q in qs:
            if q.show:
                if q.list_name == str(self.model._meta):
                    field = self.model._meta.get_field(q.field_name)
                    field_names.append(q.field_name)
                    verbose_field_names.append(
                        gen_field_ver_name(field.verbose_name))
        context = {
            'field_names': field_names,
            'verbose_field_names': verbose_field_names,
        }
        return context

    def get_queryset(self):
        account = self.request.user.profile.account
        qs = self.model.objects.filter(account=account)
        return qs

    def get_modelformset(self):
        modelformset = modelformset_factory(
            self.model,
            form=self.form,
            fields=self.get_fields()['field_names'],
            formset=self.formset,
            extra=self.extra,
        )
        return modelformset

    def get_context_data(self, *args, **kwargs):
        context = {
            'btn_back': self.btn_back,
            'btn_save': self.btn_save,
            'btn_custom': self.btn_custom,
            'page_title': self.page_title,
            'nav_link': self.nav_link,
            'detail_url': self.detail_url,
            'write_check': write_check(self.request.user)
        }
        try:
            context['fields'] = self.get_fields()['verbose_field_names']
        except KeyError:
            pass
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        formset_inst = self.get_modelformset()
        context['formset'] = formset_inst(queryset=self.get_queryset())
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset_inst = self.get_modelformset()
        formset = formset_inst(request.POST, queryset=self.get_queryset())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i in instances:
                i.account = request.user.profile.account
                i.save()
            if self.set_redirect:
                return redirect(self.get_redirect_url())
            else:
                return redirect(self.redirect_url)
