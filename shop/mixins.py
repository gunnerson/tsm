from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.views.generic.edit import UpdateView
from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django.core.exceptions import FieldError


class ObjectView(UpdateView):
    is_create = False

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None


class FormSetView():
    model = None
    form_class = None
    formset = BaseModelFormSet
    btn_back = True
    btn_save = True
    filter_bar = False
    page_title = 'List of records'
    nav_link = 'List'
    detail_url = ''
    template_name = 'shop/listview.html'
    redirect_url = '.'
    extra = 1
    fields = ()
    field_names = ()

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

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.filter_bar:
            query = self.request.GET.get('query', None)
            if query:
                qs = self.model.objects.search(
                    query,
                    self.model.__name__,
                )
            if not self.request.GET.get('term', None):
                try:
                    qs = qs.exclude(status='T')
                except FieldError:
                    pass
        return qs

    def get_form_kwargs(self):
        return {}

    def get_modelformset(self, data=None):
        modelformset = modelformset_factory(
            self.model,
            form=self.form_class,
            fields=self.fields,
            formset=self.formset,
            extra=self.extra,
        )
        return modelformset(data, queryset=self.get_queryset(),
                            form_kwargs=self.get_form_kwargs())

    def get_context_data(self, *args, **kwargs):
        context = {
            'btn_back': self.btn_back,
            'btn_save': self.btn_save,
            'page_title': self.page_title,
            'nav_link': self.nav_link,
            'detail_url': self.detail_url,
        }
        try:
            context['fields'] = self.field_names
        except KeyError:
            pass
        if 'formset' in kwargs:
            context['formset'] = kwargs['formset']
        else:
            context['formset'] = self.get_modelformset()
        if self.filter_bar:
            context['filter_bar'] = True
            context['query'] = self.request.GET.get('query', None)
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
        if formset.is_valid():
            formset.save()
            return redirect(self.redirect_url)
        else:
            return self.render_to_response(
                self.get_context_data(formset=formset))


class OrderSelect(forms.Select):

    def __init__(self, *args, **kwargs):
        self.exclude = kwargs.pop('exclude')
        return super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
        if option['value'] in self.exclude:
            option['attrs']['style'] = 'display: none;'
        return option
