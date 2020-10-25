from django import forms
from .models import EventListing

class EventForm(forms.ModelForm):
#     title = forms.CharField(label='Event Title', max_length=30)
#     description = forms.CharField(label='Description', max_length=500)
#     address = forms.CharField(label='Address', max_length=40)


    class Meta:
        model = EventListing
        fields = "__all__"
        exclude = ['company', 'now']

class UpdateEventForm(forms.ModelForm):

    class Meta:
        model = EventListing
        fields = "__all__"
        exclude = ['company', 'now']

