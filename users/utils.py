from django.http import HttpResponse

from invent.models import Truck, Trailer


def gen_field_ver_name(str):
    return str.replace("_", " ").capitalize()


def gen_list_ver_name(str):
    return str.split('.')[1].capitalize()


def generate_listcolshow(request, model):
    from django.db import IntegrityError
    from .models import ListColShow
    user = request.user
    list_name = gen_list_ver_name(str(model._meta))
    fields = model._meta.get_fields()
    for f in fields:
        if f.name != 'id':
            try:
                ListColShow(
                    profile=user.profile,
                    list_name=list_name,
                    field_name=gen_field_ver_name(f.verbose_name),
                ).save()
            except AttributeError:
                try:
                    ListColShow(
                        profile=user.profile,
                        list_name=list_name,
                        field_name=gen_field_ver_name(f.name),
                    ).save()
                except IntegrityError:
                    pass
            except IntegrityError:
                pass
    try:
        if model == Truck:
            ListColShow(
                profile=user.profile,
                list_name=list_name,
                field_name='Trailer',
            ).save()
        elif model == Trailer:
            ListColShow(
                profile=user.profile,
                list_name=list_name,
                field_name='Truck',
            ).save()
    except IntegrityError:
        pass


def generate_profile(request):
    from invent.models import Trailer, Truck
    from contacts.models import Driver, Company
    generate_listcolshow(request, Truck)
    generate_listcolshow(request, Trailer)
    generate_listcolshow(request, Driver)
    generate_listcolshow(request, Company)
    return HttpResponse('Operation successful...')
