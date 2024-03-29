from users.models import ListColShow
from users.utils import gen_field_ver_name


def get_summary_context(qs, profile, context):
    lcs = ListColShow.objects.filter(profile=profile, show=True)
    checked_field_names = {
        'invent.truck': [],
        'invent.trailer': [],
    }
    for lc in lcs:
        if lc.list_name != 'invent.company':
            checked_field_names[lc.list_name].append(lc.field_name)
    obj_list = []
    field_names = []
    get_truck_names = True
    get_trailer_names = True
    for q in qs:
        obj = [('truck_id', q.id), ]
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
        obj_list.append(obj)
        get_truck_names = False
    context['object_list'] = obj_list
    context['field_names'] = field_names
    return context


def get_font_classes(font_size, context):
    if font_size == 'S':
        context['font_class'] = 'font-small'
    elif font_size == 'L':
        context['font_class'] = 'font-large'
    else:
        context['font_class'] = 'font-medium'
    return context


def model_to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields:
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[gen_field_ver_name(f.verbose_name)] = f.value_from_object(instance)
    return data
