
from django.views.generic.edit import UpdateView


class ObjectView(UpdateView):
    is_create = False

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None
