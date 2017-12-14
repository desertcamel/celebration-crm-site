from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.company_name)

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s' % (self.branch_name)

class Customer(models.Model):
    phone_number = models.IntegerField(null=True)
    customer_name = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        return '%s' % (self.customer_name)


class Occassion(models.Model):
    occassion_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return '%s' % (self.occassion_name)


class Order(models.Model):
    Company = models.ForeignKey(Company, blank=True, null=True)
    Branch = models.ForeignKey(Branch, blank=True, null=True)
    Customer = models.ForeignKey(Customer, blank=True, null=True)
    Occassion = models.ForeignKey(Occassion, blank=True, null=True)
    Order_Date = models.DateField( blank=True, null=True)
    Order_No = models.IntegerField(null=True, blank=True)
    Total_Amount = models.FloatField(null=True, blank=True)
    Delivery_Time = models.CharField(max_length=100, blank=True)
    Delivery_Mode = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s for %s' % (self.Order_No, self.Total_Amount)


class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/%Y')


"""
class Order(models.Model):
    Branch = models.CharField(max_length=100, blank=True)
    Order_Date = models.DateField( blank=True, null=True)
    Customer = models.CharField(max_length=100, blank=True)
    Order_No = models.IntegerField(null=True, blank=True)
    Contact_No = models.IntegerField(null=True, blank=True)
    Total_Amount = models.FloatField(null=True, blank=True)
    Delivery_Time = models.CharField(max_length=100, blank=True)
    Delivery_Mode = models.CharField(max_length=100, blank=True)
    Occassion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s' % (self.order_number)
"""