from django.forms import ModelForm
from .models import *

class BookEditForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UpdateStatusForm(ModelForm):
    class Meta:
        model = Borrowed
        fields = ['status']