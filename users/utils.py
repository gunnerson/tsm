from django.http import HttpResponse


def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def account_active(user):
    return user.profile.account.is_active()


def has_access(user, group_name):
    return has_group(user, group_name) and account_active(user)


def not_empty(param):
    return param != '' and param is not None


def gen_field_ver_name(str):
    return str.replace("_", " ").capitalize()


def gen_list_ver_name(str):
    return str.split('.')[1].capitalize()


def generate_listcolshow(request, model):
    from invent.models import Truck, Trailer
    from django.db import IntegrityError
    from .models import ListColShow
    user = request.user
    list_name = gen_list_ver_name(str(model._meta))
    fields = model._meta.get_fields()
    for f in fields:
        if f.name not in ('id', 'account'):
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
