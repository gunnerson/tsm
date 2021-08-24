from .models import Driver
from users.models import ListColShow
from users.utils import gen_field_ver_name


def get_summary_context(qs, profile, context):
    lcs = ListColShow.objects.filter(profile=profile, show=True)
    checked_field_names = {
        'invent.truck': [],
        'invent.trailer': [],
        'invent.driver': [],
    }
    for lc in lcs:
        if lc.list_name != 'invent.company':
            checked_field_names[lc.list_name].append(lc.field_name)
    obj_list = []
    field_names = []
    get_truck_names = True
    get_trailer_names = True
    get_driver_names = True
    for q in qs:
        obj = [('truck_id', q.id), ]
        field_names.append('')
        for checked_field in checked_field_names['invent.truck']:
            field = q._meta.get_field(checked_field)
            field_verbose_name = gen_field_ver_name(field.verbose_name)
            obj.append((field_verbose_name, getattr(q, field.name)))
            if get_truck_names:
                field_names.append(field_verbose_name)
        try:
            trailer = q.driver.trailer
            if trailer is not None:
                obj.append(('trailer_id', trailer.id))
                field_names.append('')
                for checked_field in checked_field_names['invent.trailer']:
                    field = trailer._meta.get_field(checked_field)
                    field_verbose_name = gen_field_ver_name(field.verbose_name)
                    obj.append(
                        (field_verbose_name, getattr(trailer, field.name)))
                    if get_trailer_names:
                        field_names.append(field_verbose_name)
                get_trailer_names = False
            else:
                obj.append(('trailer_id', ''))
                for i in range(0, len(checked_field_names['invent.trailer'])):
                    obj.append(('', ''))
        except (Driver.DoesNotExist):
            obj.append(('trailer_id', ''))
            for i in range(0, len(checked_field_names['invent.trailer'])):
                obj.append(('', ''))
        try:
            driver = q.driver
            if driver is not None:
                obj.append(('driver_id', driver.id))
                field_names.append('')
                for checked_field in checked_field_names['invent.driver']:
                    field = driver._meta.get_field(checked_field)
                    field_verbose_name = gen_field_ver_name(field.verbose_name)
                    if field_verbose_name not in ('Truck', 'Trailer'):
                        obj.append(
                            (field_verbose_name, getattr(driver, field.name)))
                        if get_driver_names:
                            field_names.append(field_verbose_name)
                get_driver_names = False
            else:
                obj.append(('driver_id', ''))
                for i in range(2, len(checked_field_names['invent.driver'])):
                    obj.append(('', ''))
        except (Driver.DoesNotExist):
            obj.append(('driver_id', ''))
            for i in range(2, len(checked_field_names['invent.driver'])):
                obj.append(('', ''))
        obj_list.append(obj)
        get_truck_names = False
    context['object_list'] = obj_list
    context['field_names'] = field_names
    return context
