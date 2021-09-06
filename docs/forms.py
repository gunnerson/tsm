from .mixins import ImageForm, FileForm

from .models import TruckImage, TrailerImage, TruckDocument, TrailerDocument, \
    DriverDocument, CompanyDocument


class TruckImageForm(ImageForm):

    class Meta:
        model = TruckImage
        exclude = ('origin',)


class TrailerImageForm(ImageForm):

    class Meta:
        model = TrailerImage
        exclude = ('origin',)


class TruckDocumentForm(FileForm):

    class Meta:
        model = TruckDocument
        exclude = ('origin',)


class TrailerDocumentForm(FileForm):

    class Meta:
        model = TrailerDocument
        exclude = ('origin',)


class DriverDocumentForm(FileForm):

    class Meta:
        model = DriverDocument
        exclude = ('origin',)


class CompanyDocumentForm(FileForm):

    class Meta:
        model = CompanyDocument
        exclude = ('origin',)
