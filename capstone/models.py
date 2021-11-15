from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.email

class PlanSeguro(models.Model):
    plan = models.TextField(max_length=50)
    coverage = models.IntegerField(max_length=20)
    deducible = models.IntegerField(max_length=20)
    company = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"plan:{self.plan} coverage:{self.coverage}"

class Contact(models.Model):
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creador")
    name = models.TextField(max_length=200)
    phone = models.IntegerField(max_length=20)
    email = models.TextField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    iscustomer = models.BooleanField(default=False)
    
    def __str__(self):
        return f"name:{self.name} email{self.email}"
    

class Customer(models.Model):
    contacto = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='info_contact')
    planes = models.ManyToManyField(PlanSeguro, blank=True, related_name='customers')
    timecustomer = models.DateTimeField(auto_now_add=True)
    payment = models.FloatField(max_length=10, blank= True, null=True)
    age = models.IntegerField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"contacto:{self.contacto.name} - payment:{self.payment}"
