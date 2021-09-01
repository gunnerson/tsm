from .mixins import ImageForm

from .models import OrderImage, InspectionImage, TruckImage, TrailerImage


class OrderImageForm(ImageForm):
    class Meta:
        model = OrderImage
        exclude = ('origin',)


class InspectionImageForm(ImageForm):
    class Meta:
        model = InspectionImage
        exclude = ('origin',)


class TruckImageForm(ImageForm):

    class Meta:
        model = TruckImage
        exclude = ('origin',)


class TrailerImageForm(ImageForm):

    class Meta:
        model = TrailerImage
        exclude = ('origin',)
