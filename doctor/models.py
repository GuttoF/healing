from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Speciality(models.Model):
    speciality = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="icons", null=True, blank=True)

    def __str__(self):
        return self.speciality


class DoctorData(models.Model):
    crm = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    number = models.IntegerField()
    rg = models.ImageField(upload_to="rgs")
    cim = models.ImageField(upload_to="cim")
    picture = models.ImageField(upload_to="profile_pics")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    speciality = models.ForeignKey(
        Speciality, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    bill = models.FloatField(default=100)

    def __str__(self):
        return self.user.username
