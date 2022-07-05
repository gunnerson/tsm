from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from pathlib import Path
from django import forms


class ImageCreateView(CreateView):
    origin_model = None
    folder_name = 'temp'
    template_name = 'docs/form.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['origin_id'] = self.kwargs['pk']
        context['btn_save'] = True
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        origin_id = self.kwargs['pk']
        origin = self.origin_model.objects.get(id=origin_id)
        date = self.object.date
        files = self.request.FILES.getlist('image')
        for f in files:
            self.model.objects.create(origin=origin, image=f, date=date)
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        origin_id = self.kwargs['pk']
        origin = self.origin_model.objects.get(id=origin_id)
        return origin.get_absolute_url()


class ImageListView(ListView):
    origin_model = None
    template_name = 'docs/gallery.html'
    key_url = None

    def get_origin(self):
        return self.origin_model.objects.get(id=self.kwargs['pk'])

    def post(self, *args, **kwargs):
        qs = self.get_queryset()
        for q in qs:
            if self.request.POST.get(str(q.id), None):
                q.delete()
        return redirect('.')

    def get_context_data(self, *args, **kwargs):
        origin = self.get_origin()
        context = super().get_context_data(*args, **kwargs)
        context['btn_del'] = True
        context['btn_key'] = True
        context['key_url'] = self.key_url
        context['key_id'] = origin.id
        return context


class ImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields["image"].widget.attrs.update({'multiple': 'True'})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class DocumentCreateView(CreateView):
    origin_model = None
    folder_name = 'temp'
    template_name = 'docs/form.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['origin_id'] = self.kwargs['pk']
        context['btn_save'] = True
        return context

    def get_redirect_url(self):
        origin_id = self.kwargs['pk']
        origin = self.origin_model.objects.get(id=origin_id)
        return origin.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        origin_id = self.kwargs['pk']
        self.object.origin = self.origin_model.objects.get(id=origin_id)
        file_name = '#' + self.object.origin.fleet_number + '_' + self.object.get_category_display().lower()
        if self.object.description:
            file_name += '_' + self.object.description.replace(' ', '_').lower().strip()
        file_ext = Path(self.object.file.name).suffixes
        self.object.file.name = 'doc/{0}/{1}/{2}{3}'.format(
            self.folder_name, origin_id, file_name, file_ext)
        self.object.save()
        return redirect(self.get_redirect_url())


class DocumentListView(ListView):
    origin_model = None
    template_name = 'docs/files.html'
    key_url = None

    def get_origin(self):
        return self.origin_model.objects.get(id=self.kwargs['pk'])

    def post(self, *args, **kwargs):
        qs = self.get_queryset()
        for q in qs:
            if self.request.POST.get(str(q.id), None):
                q.delete()
        return redirect('.')

    def get_context_data(self, *args, **kwargs):
        origin = self.get_origin()
        context = super().get_context_data(*args, **kwargs)
        context['btn_del'] = True
        context['btn_key'] = True
        context['key_url'] = self.key_url
        context['key_id'] = origin.id
        return context


class FileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
