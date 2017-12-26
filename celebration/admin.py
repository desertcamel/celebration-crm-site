from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Company, Customer, Branch, Order, Occassion

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Occassion)
admin.site.register(Customer)
admin.site.register(Order)

from .models import Profile
admin.site.register(Profile)

