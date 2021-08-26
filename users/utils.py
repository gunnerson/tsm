from django.http import HttpResponse


def admin_check(user):
    try:
        return (user.profile.level == 'A'
                and user.profile.account.is_active())
    except AttributeError:
        return False


def write_check(user):
    try:
        return (user.profile.level in ('A', 'W')
                and user.profile.account.is_active())
    except AttributeError:
        return False


def read_check(user):
    try:
        return (user.profile.level in ('A', 'W', 'R')
                and user.profile.account.is_active())
    except AttributeError:
        return False


def not_empty(param):
    return param != '' and param is not None


def gen_field_ver_name(str):
    new_str = str[0].capitalize() + str[1:]
    return new_str.replace("_", " ")


def gen_list_ver_name(str):
    return str.split('.')[1].capitalize()


def generate_listcolshow(profile, model):
    from invent.models import Truck, Trailer, Driver, Company
    from django.db import IntegrityError
    from .models import ListColShow
    list_name = str(model._meta)
    fields = model._meta.get_fields()
    i = 1
    if model == Truck or model == Trailer:
        exclude = ('id', 'driver')
    elif model == Driver:
        exclude = ('id')
    elif model == Company:
        exclude = ('id', 'driver', 'owned_trucks', 'insured_trucks',
                   'owned_trailers', 'insured_trailers')
    for f in fields:
        if f.name not in exclude:
            try:
                ListColShow(
                    profile=profile,
                    list_name=list_name,
                    field_name=f.name,
                    order=i,
                ).save()
                i += 1
            except IntegrityError:
                pass


def generate_profile(profile):
    from invent.models import Trailer, Truck, Driver, Company
    generate_listcolshow(profile, Truck)
    generate_listcolshow(profile, Trailer)
    generate_listcolshow(profile, Driver)
    generate_listcolshow(profile, Company)
    return HttpResponse('Operation successful...')


def generate_su_profile(request):
    from invent.models import Trailer, Truck, Driver, Company
    from .models import ListColShow
    profile = request.user.profile
    ListColShow.objects.filter(profile=profile).delete()
    generate_listcolshow(profile, Truck)
    generate_listcolshow(profile, Trailer)
    generate_listcolshow(profile, Driver)
    generate_listcolshow(profile, Company)
    return HttpResponse('Operation successful...')


# def get_columns(user):
#     from .models import ListColShow
#     from invent.models import Truck, Trailer, Driver
#     qs = ListColShow.objects.filter(
#         profile=user.profile,
#     )
#     context = {}
#     truck_field_names = []
#     trailer_field_names = []
#     driver_field_names = []
#     truck_verbose_field_names = []
#     trailer_verbose_field_names = []
#     driver_verbose_field_names = []
#     for q in qs:
#         if q.show:
#             if q.list_name == 'invent.truck':
#                 field = Truck._meta.get_field(q.field_name)
#                 truck_field_names.append(q.field_name)
#                 truck_verbose_field_names.append(
#                     gen_field_ver_name(field.verbose_name))
#             elif q.list_name == 'invent.trailer':
#                 field = Trailer._meta.get_field(q.field_name)
#                 trailer_field_names.append(q.field_name)
#                 trailer_verbose_field_names.append(
#                     gen_field_ver_name(field.verbose_name))
#             elif q.list_name == 'contacts.driver':
#                 field = Driver._meta.get_field(q.field_name)
#                 driver_field_names.append(q.field_name)
#                 driver_verbose_field_names.append(
#                     gen_field_ver_name(field.verbose_name))
#             else:
#                 pass
#     context['truck_field_names'] = truck_field_names
#     context['trailer_field_names'] = trailer_field_names
#     context['driver_field_names'] = driver_field_names
#     context['truck_verbose_field_names'] = truck_verbose_field_names
#     context['trailer_verbose_field_names'] = trailer_verbose_field_names
#     context['driver_verbose_field_names'] = driver_verbose_field_names
#     return context
