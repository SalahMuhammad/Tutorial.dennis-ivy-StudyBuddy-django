from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # all fields from room model
        exclude = ['host', 'participants']  # or you can specifay fields
