from django.contrib import admin

# Register your models here.
from .models import Company, Customer, Branch, Order, Occassion

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Occassion)
admin.site.register(Customer)
admin.site.register(Order)