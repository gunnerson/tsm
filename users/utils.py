from django.http import HttpResponse


def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def account_active(user):
    return user.profile.account.is_active()


def has_access(user, group_name):
    return has_group(user, group_name) and account_active(user)


def write_check(user):
    return (user.groups.filter(name='write').exists()
            and user.profile.account.is_active())

def read_check(user):
    return (user.groups.filter(name='read').exists()
            and user.profile.account.is_active())

def not_empty(param):
    return param != '' and param is not None


def gen_field_ver_name(str):
    new_str = str[0].capitalize() + str[1:]
    return new_str.replace("_", " ")


def gen_list_ver_name(str):
    return str.split('.')[1].capitalize()


def get_columns(user):
    from .models import ListColShow
    from invent.models import Truck, Trailer
    from contacts.models import Driver
    qs = ListColShow.objects.filter(
        profile=user.profile,
    )
    context = {}
    truck_field_names = []
    trailer_field_names = []
    driver_field_names = []
    truck_verbose_field_names = []
    trailer_verbose_field_names = []
    driver_verbose_field_names = []
    for q in qs:
        if q.show:
            if q.list_name == 'invent.truck':
                field = Truck._meta.get_field(q.field_name)
                truck_field_names.append(q.field_name)
                truck_verbose_field_names.append(
                    gen_field_ver_name(field.verbose_name))
            elif q.list_name == 'invent.trailer':
                field = Trailer._meta.get_field(q.field_name)
                trailer_field_names.append(q.field_name)
                trailer_verbose_field_names.append(
                    gen_field_ver_name(field.verbose_name))
            elif q.list_name == 'contacts.driver':
                field = Driver._meta.get_field(q.field_name)
                driver_field_names.append(q.field_name)
                driver_verbose_field_names.append(
                    gen_field_ver_name(field.verbose_name))
            else:
                pass
    context['truck_field_names'] = truck_field_names
    context['trailer_field_names'] = trailer_field_names
    context['driver_field_names'] = driver_field_names
    context['truck_verbose_field_names'] = truck_verbose_field_names
    context['trailer_verbose_field_names'] = trailer_verbose_field_names
    context['driver_verbose_field_names'] = driver_verbose_field_names
    return context

def generate_listcolshow(request, model):
    from invent.models import Truck, Trailer
    from contacts.models import Driver
    from django.db import IntegrityError
    from .models import ListColShow
    user = request.user
    list_name = str(model._meta)
    fields = model._meta.get_fields()
    if model == Truck:
        for f in fields:
            if f.name not in ('id', 'account', 'driver'):
                try:
                    ListColShow(
                        profile=user.profile,
                        list_name=list_name,
                        field_name=f.name,
                    ).save()
                except IntegrityError:
                    pass
    elif model == Trailer:
        for f in fields:
            if f.name not in ('id', 'account', 'driver'):
                try:
                    ListColShow(
                        profile=user.profile,
                        list_name=list_name,
                        field_name=f.name,
                    ).save()
                except IntegrityError:
                    pass
    elif model == Driver:
        for f in fields:
            if f.name not in ('id', 'account', 'first_name', 'last_name'):
                try:
                    ListColShow(
                        profile=user.profile,
                        list_name=list_name,
                        field_name=f.name,
                    ).save()
                except IntegrityError:
                    pass


def generate_profile(request):
    from invent.models import Trailer, Truck
    from contacts.models import Driver
    generate_listcolshow(request, Truck)
    generate_listcolshow(request, Trailer)
    generate_listcolshow(request, Driver)
    return HttpResponse('Operation successful...')
