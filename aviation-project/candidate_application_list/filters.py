import django_filters
from django_filters import CharFilter
from apply.models import *
from users.models import *
from django.db import models

class ApplicantFilter(django_filters.FilterSet):
    name = CharFilter(field_name='applicant__name',lookup_expr='icontains', label='applicant')

    class Meta:
        model = Application
        fields = ['applicant']

