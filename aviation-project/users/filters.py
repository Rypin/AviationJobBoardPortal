import django_filters
from django_filters import CharFilter, MultipleChoiceFilter
from .models import Users, Skill
from django.db import models

class UsersFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Name')

    class Meta:
        model = Users
        fields = ['name', 'skills']

