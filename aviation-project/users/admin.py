from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
from .models import Users
from .models import workExperience
from .models import educationExperience
from .models import CompanyProfile

# Register your models here.
admin.site.register(Profile)
admin.site.register(CompanyProfile)
admin.site.register(Users)
admin.site.register(workExperience)
admin.site.register(educationExperience)
