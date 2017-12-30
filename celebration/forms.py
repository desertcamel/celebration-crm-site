from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime #for checking renewal date range.
from .models import Company, Customer, Branch, Order, Occassion, Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


# USER AND PROFILE FORMS
from .models import Profile
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'company_name')

# SEARCH FORMS

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'Company', 'Branch', 'Occassion'
