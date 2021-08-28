from django.forms import modelformset_factory, BaseModelFormSet

from .models import JobItem
from .forms import JobItemForm


def get_job_forms(order, data=None):
    JobModelFormset = modelformset_factory(
        JobItem,
        form=JobItemForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    qs = order.jobitem_set.all()
    return JobModelFormset(data, queryset=qs)
