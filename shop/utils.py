from django.forms import modelformset_factory, BaseModelFormSet
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import OrderJob, OrderPart, Part, PurchaseItem, PartPlace
from invent.models import Truck, Trailer
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


def get_part_forms(order, data=None, exclude=True):
    ModelFormset = modelformset_factory(
        OrderPart,
        form=OrderPartForm,
        fields='__all__',
        formset=BaseModelFormSet,
    )
    assigned_parts_ids = []
    exclude_ids = []
    part_ids = []
    if exclude and order.truck:
        part_places = order.truck.partplace_set.all()
        for p in part_places:
            assigned_parts_ids.append(p.part.id)
            for rp in p.part.replaces.all():
                assigned_parts_ids.append(rp.id)
            for rp in p.part.part_set.all():
                assigned_parts_ids.append(rp.id)
            try:
                for rp in p.part.part_set.last().replaces.exclude(id=p.part.id):
                    assigned_parts_ids.append(rp.id)
            except AttributeError:
                pass
    elif exclude and order.trailer:
        part_places = order.trailer.partplace_set.all()
        for p in part_places:
            assigned_parts_ids.append(p.part.id)
            for rp in p.part.replaces.all():
                assigned_parts_ids.append(rp.id)
            for rp in p.part.part_set.all():
                assigned_parts_ids.append(rp.id)
            try:
                for rp in p.part.part_set.last().replaces.exclude(id=p.part.id):
                    assigned_parts_ids.append(rp.id)
            except AttributeError:
                pass
    qs = order.orderpart_set.all()
    for q in qs:
        if q.part.id not in exclude_ids:
            exclude_ids.append(q.part.id)
        part_ids.append(q.part.id)
    for j in order.orderjob_set.all():
        for pt in j.job.part_types.all():
            for p in pt.part_set.all():
                if exclude:
                    if p.id in assigned_parts_ids and p.id not in part_ids:
                        part_ids.append(p.id)
                else:
                    if p.id not in part_ids:
                        part_ids.append(p.id)
                if p.stock == 0:
                    exclude_ids.append(p.id)
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
            partplace, created = PartPlace.objects.get_or_create(
                part=inst.part, truck=inst.order.truck)
        elif inst.order.trailer:
            inst.part.trailers.add(inst.order.trailer)
            partplace, created = PartPlace.objects.get_or_create(
                part=inst.part, trailer=inst.order.trailer)


def assign_to_101():
    parts = Part.objects.all()
    t = Truck.objects.get(id=40)
    for p in parts:
        try:
            PartPlace.objects.get(part=p, truck=t)
        except ObjectDoesNotExist:
            PartPlace(part=p, truck=t).save()
    return HttpResponse('Operation successful...')
