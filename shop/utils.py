from django.forms import modelformset_factory, BaseModelFormSet

from .models import OrderJob
from .forms import OrderJobForm


def get_job_forms(order, data=None):
    JobModelFormset = modelformset_factory(
        OrderJob,
        form=OrderJobForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    qs = order.orderjob_set.all()
    return JobModelFormset(data, queryset=qs)
