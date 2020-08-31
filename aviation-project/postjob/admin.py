import json
from django.contrib import admin
from .models import Jobtype, Jobform
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

# Register your models here.


admin.site.register(Jobtype)
#admin.site.register(Jobform)


@admin.register(Jobform)
class JobformAdmin(admin.ModelAdmin): formfield_overrides = {
    map_fields.AddressField: { 'widget':
    map_widgets.GoogleMapsAddressWidget(attrs={
      'data-autocomplete-options': json.dumps({ 'types': ['geocode',
      'establishment'], 'componentRestrictions': {
                  'country': 'us'
              }
          })
      })
    },
}
# class JobformAdmin(admin.ModelAdmin):
#     list_display = ['title','postdate', 'posttime', 'deadlinedate', 'deadlinetime', 'open', 'datenow', 'timenow']
# @admin.register(Jobform)
# class JobformAdmin(admin.ModelAdmin):
#     list_display = ['title','postdate', 'posttime', 'deadlinedate', 'deadlinetime', 'open']
