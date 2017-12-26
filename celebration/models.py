from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.company_name)

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])
    

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    company_name = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return '%s' % (self.branch_name)

    def get_absolute_url(self):
        return reverse('branch-detail', args=[str(self.id)])


class Customer(models.Model):
    phone_number = models.IntegerField(null=True)
    customer_name = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return '%s' % (self.customer_name)

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.id)])


class Occassion(models.Model):
    occassion_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return '%s' % (self.occassion_name)

    def get_absolute_url(self):
        return reverse('occassion-detail', args=[str(self.id)])


class Order(models.Model):
    Company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    Branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.SET_NULL)
    Customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    Occassion = models.ForeignKey(Occassion, blank=True, null=True, on_delete=models.SET_NULL)
    Order_Date = models.DateField( blank=True, null=True)
    Order_No = models.IntegerField(null=True, blank=True)
    Total_Amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s for %s' % (self.Order_No, self.Total_Amount)



class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/%Y')




# CREATE USER PROFILE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % (self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()