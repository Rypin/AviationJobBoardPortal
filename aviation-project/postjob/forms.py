import json
from django import forms
from .models import Jobform
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class DateInput(forms.DateInput):
    input_type = "date"

class TimeInput(forms.TimeInput):
    input_type = "time"

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

class PostingForm(forms.ModelForm):
    class Meta:
        model = Jobform
        fields = "__all__"
        labels = {
            'title': 'Title', 
            'decription': 'Description', 
            'jobtype': 'Job Type', 
            'postdate': 'Post Date', 
            'deadlinedate': 'Deadline Date',
            'posttime': 'Post Time', 
            'deadlinetime': 'Deadline Time'
            }
        widgets = {
            'title': forms.TextInput(attrs={'size':20, 'placeholder': 'e.g. Title'}),
            'description': forms.Textarea(attrs={'rows':10, 'cols':150}),
            'postdate': DateInput(),
            'posttime': TimeInput(),
            'deadlinedate': DateInput(),
            'deadlinetime': TimeInput(),
            'address': map_widgets.GoogleMapsAddressWidget(attrs={'data-autocomplete-options': json.dumps({'types': ['geocode', 'establishment'], 'componentRestrictions': {'country': 'us'}}), 'size':50,}),
            'geolocation': map_widgets.GoogleMapsAddressWidget(attrs = {'hidden':True}),
            }

#
#     #jobtype = forms.ModelChoiceField(queryset=Jobtype.objects, empty_label=None,  widget=forms.RadioSelect)
#
#     title = forms.TextInput(attrs={'size':150, 'placeholder': 'e.g. Senior Manager'}),
#     description = forms.Textarea(attrs={'rows':10, 'cols':150}),
#     zipcode = forms.TextInput(attrs={'size':150, 'placeholder': 'e.g. 11111'}),
#     # 'post': DateTimeInput(),
#     # 'deadline': DateTimeInput(),
#     postdate = DateInput(),
#     posttime = TimeInput(),
#     deadlinedate = DateInput(),
#     deadlinetime = TimeInput(),
#
#     class Meta:
#         model = Jobform
#         fields = ['title', 'description', 'jobtype', 'postdate', 'deadlinedate', 'posttime', 'deadlinetime']

class UpdateJobForm(forms.ModelForm):
    title = forms.TextInput(attrs={'size': 150, 'placeholder': 'e.g. Senior Manager'}),
    description = forms.Textarea(attrs={'rows': 10, 'cols': 150}),
    zipcode = forms.TextInput(attrs={'size': 150, 'placeholder': 'e.g. 11111'}),
    postdate = DateInput(),
    posttime = TimeInput(),
    deadlinedate = DateInput(),
    deadlinetime = TimeInput(),

    class Meta:
        model = Jobform
        fields = ['title', 'description', 'jobtype', 'postdate', 'deadlinedate', 'posttime', 'deadlinetime']
