from django.contrib import admin

# Register your models here.
from .models import Speciality, DoctorData
# Register your models here.
admin.site.register(Speciality)
admin.site.register(DoctorData)