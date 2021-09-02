from users.mixins import WriteCheckMixin

from .models import OrderImage, InspectionImage, TruckImage, TrailerImage, \
    TruckDocument, TrailerDocument, DriverDocument, CompanyDocument
from .forms import OrderImageForm, InspectionImageForm, TruckImageForm, \
    TrailerImageForm, TruckDocumentForm, TrailerDocumentForm, \
    DriverDocumentForm, CompanyDocumentForm
from .mixins import ImageCreateView, ImageListView, DocumentCreateView, \
    DocumentListView
from shop.models import Order, Inspection
from invent.models import Truck, Trailer, Driver, Company


class OrderImageView(WriteCheckMixin, ImageCreateView):
    model = OrderImage
    form_class = OrderImageForm
    origin_model = Order
    folder_name = 'orders'


class OrderImageListView(WriteCheckMixin, ImageListView):
    model = OrderImage
    origin_model = Order
    key_url = "shop:order"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.orderimage_set.all()


class InspectionImageView(WriteCheckMixin, ImageCreateView):
    model = InspectionImage
    form_class = InspectionImageForm
    origin_model = Inspection
    folder_name = 'inspections'


class InspectionImageListView(WriteCheckMixin, ImageListView):
    model = InspectionImage
    origin_model = Inspection
    key_url = "shop:inspection"

    def get_queryset(self):
        origin = self.get_origin()
        return origin.inspectionimage_set.all()


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
