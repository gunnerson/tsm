from users.mixins import WriteCheckMixin

from .models import TruckImage, TrailerImage, TruckDocument, TrailerDocument, \
    DriverDocument, CompanyDocument
from .forms import TruckImageForm, TrailerImageForm, TruckDocumentForm, \
    TrailerDocumentForm, DriverDocumentForm, CompanyDocumentForm
from .mixins import ImageCreateView, ImageListView, DocumentCreateView, \
    DocumentListView
from invent.models import Truck, Trailer, Driver, Company


class TruckImageView(WriteCheckMixin, ImageCreateView):
    model = TruckImage
    form_class = TruckImageForm
    origin_model = Truck
    folder_name = 'trucks'


class TruckImageListView(WriteCheckMixin, ImageListView):
    model = TruckImage
    origin_model = Truck
    key_url = "invent:truck"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.truckimage_set.all()


class TrailerImageView(WriteCheckMixin, ImageCreateView):
    model = TrailerImage
    form_class = TrailerImageForm
    origin_model = Trailer
    folder_name = 'trailers'


class TrailerImageListView(WriteCheckMixin, ImageListView):
    model = TrailerImage
    origin_model = Trailer
    key_url = "invent:trailer"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.trailerimage_set.all()


class TruckDocumentView(WriteCheckMixin, DocumentCreateView):
    model = TruckDocument
    form_class = TruckDocumentForm
    origin_model = Truck
    folder_name = 'trucks'


class TruckDocumentListView(WriteCheckMixin, DocumentListView):
    model = TruckDocument
    origin_model = Truck
    key_url = "invent:truck"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.truckdocument_set.all()


class TrailerDocumentView(WriteCheckMixin, DocumentCreateView):
    model = TrailerDocument
    form_class = TrailerDocumentForm
    origin_model = Trailer
    folder_name = 'trailers'


class TrailerDocumentListView(WriteCheckMixin, DocumentListView):
    model = TrailerDocument
    origin_model = Trailer
    key_url = "invent:trailer"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.trailerdocument_set.all()


class DriverDocumentView(WriteCheckMixin, DocumentCreateView):
    model = DriverDocument
    form_class = DriverDocumentForm
    origin_model = Driver
    folder_name = 'drivers'


class DriverDocumentListView(WriteCheckMixin, DocumentListView):
    model = DriverDocument
    origin_model = Driver
    key_url = "invent:driver"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.driverdocument_set.all()


class CompanyDocumentView(WriteCheckMixin, DocumentCreateView):
    model = CompanyDocument
    form_class = CompanyDocumentForm
    origin_model = Company
    folder_name = 'companies'


class CompanyDocumentListView(WriteCheckMixin, DocumentListView):
    model = CompanyDocument
    origin_model = Company
    key_url = "invent:company"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.companydocument_set.all()
