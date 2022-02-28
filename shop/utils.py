from django.forms import modelformset_factory, BaseModelFormSet

from .models import OrderJob, OrderPart, Part, PurchaseItem
from .forms import OrderJobForm, OrderPartForm, PurchaseItemForm


def get_job_forms(order, data=None):
    ModelFormset = modelformset_factory(
        OrderJob,
        form=OrderJobForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    qs = order.orderjob_set.all()
    job_ids = []
    for q in qs:
        if q.job.id not in job_ids:
            job_ids.append(q.job.id)
    return ModelFormset(data, queryset=qs, prefix='jobs',
                        form_kwargs={'exclude': job_ids})


def get_part_forms(order, data=None):
    ModelFormset = modelformset_factory(
        OrderPart,
        form=OrderPartForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    assigned_parts_ids = []
    exclude_ids = []
    part_ids = []
    if order.truck:
        part_places = order.truck.partplace_set.all()
        for p in part_places:
            assigned_parts_ids.append(p.part.id)
    elif order.trailer:
        part_places = order.trailer.partplace_set.all()
        for p in part_places:
            assigned_parts_ids.append(p.part.id)
    qs = order.orderpart_set.all()
    for q in qs:
        if q.part.id not in exclude_ids:
            exclude_ids.append(q.part.id)
        part_ids.append(q.part.id)
    for j in order.orderjob_set.all():
        # for p in j.job.parts.all():
        #     if p.id not in part_ids:
        #         part_ids.append(p.id)
        for pt in j.job.part_types.all():
            for p in pt.part_set.all():
                if p.id in assigned_parts_ids and p.id not in part_ids:
                    part_ids.append(p.id)
    parts = Part.objects.filter(id__in=part_ids)
    return ModelFormset(data, queryset=qs, prefix='parts',
                        form_kwargs={'parts': parts, 'exclude': exclude_ids})


def get_purchase_forms(order, data=None):
    ModelFormset = modelformset_factory(
        PurchaseItem,
        form=PurchaseItemForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    qs = order.purchaseitem_set.all()
    exclude_ids = []
    for q in qs:
        if q.part.id not in exclude_ids:
            exclude_ids.append(q.part.id)
    return ModelFormset(data, queryset=qs,
                        form_kwargs={'exclude': exclude_ids})


def link_with_part(inst, remove=None):
    if remove:
        if inst.order.truck:
            inst.part.trucks.remove(inst.order.truck)
        elif inst.order.trailer:
            inst.part.trailers.remove(inst.order.trailer)
    else:
        if inst.order.truck:
            inst.part.trucks.add(inst.order.truck)
        elif inst.order.trailer:
            inst.part.trailers.add(inst.order.trailer)



