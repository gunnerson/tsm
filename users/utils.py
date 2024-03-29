from django.http import HttpResponse


def admin_check(user):
    return user.profile.level == 'A'


def write_check(user):
    return user.profile.level in ('A', 'W')


def read_check(user):
    try:
        return user.profile.level in ('A', 'W', 'R')
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
    from invent.models import Truck, Trailer, Company
    from django.db import IntegrityError
    from .models import ListColShow
    list_name = str(model._meta)
    fields = model._meta.get_fields()
    i = 1
    if model == Truck or model == Trailer:
        exclude = ('id', 'order', 'part', 'truck_pms', 'truckimage',
                   'truckdocument', 'trailer_pms', 'trailerimage',
                   'trailerdocument', 'partplace', 'kt_id', 'show')
    elif model == Company:
        exclude = ('id', 'owned_trucks', 'insured_trucks', 'order',
                   'owned_trailers', 'insured_trailers', 'purchase', 'profile',
                   'companydocument', 'show')
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
    from invent.models import Trailer, Truck, Company
    generate_listcolshow(profile, Truck)
    generate_listcolshow(profile, Trailer)
    generate_listcolshow(profile, Company)
    return HttpResponse('Operation successful...')


def generate_su_profile(request):
    from invent.models import Trailer, Truck, Company
    from .models import ListColShow
    profile = request.user.profile
    ListColShow.objects.filter(profile=profile).delete()
    generate_listcolshow(profile, Truck)
    generate_listcolshow(profile, Trailer)
    generate_listcolshow(profile, Company)
    return HttpResponse('Operation successful...')


def assign_to_101(request):
    parts = Part.objects.all()
    t = Truck.objects.get(id=40)
    for p in parts:
        try:
            PartPlace.objects.get(part=p, truck=t)
        except ObjectDoesNotExist:
            PartPlace(part=p, truck=t).save()
    return HttpResponse('Operation successful...')
