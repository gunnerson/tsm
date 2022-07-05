from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django.core.exceptions import FieldError
from django.views.generic import DetailView

from .utils import model_to_dict
from .models import Company
from users.utils import gen_field_ver_name, write_check
from users.models import ListColShow


class FormSetView():
    model = None
    form_class = None
    formset = BaseModelFormSet
    btn_save = True
    filter_bar = True
    detail_url = ''
    template_name = 'invent/listview.html'
    redirect_url = '.'
    extra = 1

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

    def __init__(self, request, **kwargs):
        self.request = request
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_fields(self):
        qs = ListColShow.objects.filter(profile=self.request.user.profile)
        field_names = []
        verbose_field_names = []
        for q in qs:
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
        request = self.request
        ours = request.GET.get('ours', None)
        our_companies = Company.objects.filter(group__in=('OU', ))
        if ours:
            qs = self.model.objects.filter(show=True)
        else:
            try:
                qs = self.model.objects.filter(owner__in=our_companies, show=True)
            except FieldError:
                pass
                qs = self.model.objects.filter(show=True)
        query = self.request.GET.get('query', None)
        if query:
            qs = self.model.objects.search(
                query,
                self.model.__name__,
                our_companies,
            )
        return qs

    def get_form_kwargs(self):
        return {}

    def get_modelformset(self, data=None):
        modelformset = modelformset_factory(
            self.model,
            form=self.form_class,
            fields=self.get_fields()['field_names'],
            formset=self.formset,
            extra=self.extra,
        )
        return modelformset(data, queryset=self.get_queryset(),
                            form_kwargs=self.get_form_kwargs())

    def get_context_data(self, *args, **kwargs):
        context = {
            'btn_save': self.btn_save,
            'detail_url': self.detail_url,
        }
        try:
            context['fields'] = self.get_fields()['verbose_field_names']
        except KeyError:
            pass
        if 'formset' in kwargs:
            context['formset'] = kwargs['formset']
        else:
            context['formset'] = self.get_modelformset()
        if self.filter_bar:
            context['filter_bar'] = True
            context['query'] = self.request.GET.get('query', None)
            context['ours'] = self.request.GET.get('ours', None)
            context['term'] = self.request.GET.get('term', None)
        return context

    def render_to_response(self, context):
        return render(
            request=self.request,
            template_name=self.template_name,
            context=context,
        )

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        formset = self.get_modelformset(request.POST)
        if formset.is_valid() and write_check(request.user):
            formset.save()
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))


class VehicleSelect(forms.Select):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        return super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
        object_id = option['value'].__str__()
        if object_id:
            obj = self.model.objects.get(id=object_id)
            try:
                obj.driver
                option['attrs']['class'] = 'choice_taken'
            except self.model.driver.RelatedObjectDoesNotExist:
                pass
        return option


class FormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class FormSetMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class InfoView(DetailView):
    image_url = None
    gallery_url = None
    doc_url = None
    files_url = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        inst = self.get_object()
        context['fields'] = model_to_dict(inst, exclude=('id'))
        context['inst_id'] = inst.id
        context['btn_image'] = True
        context['image_url'] = self.image_url
        context['image_id'] = inst.id
        context['btn_gallery'] = True
        context['gallery_url'] = self.gallery_url
        context['btn_doc'] = True
        context['doc_url'] = self.doc_url
        context['btn_files'] = True
        context['files_url'] = self.files_url
        return context
