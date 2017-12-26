from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Company, Branch, Customer, Order, Occassion, Document
from django.urls import reverse, reverse_lazy

from .forms import DocumentForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage

import pandas as pd
import csv

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_branch=Branch.objects.all().count()
    num_customers=Customer.objects.all().count()
    num_occassions=Occassion.objects.all().count()
    num_orders=Order.objects.all().count()


    # SESSION TRACKER
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'celebration/index.html',
        context={'num_branch':num_branch,'num_customers':num_customers,'num_occassions':num_occassions, 
        'num_orders':num_orders, 'num_visits':num_visits}, # num_visits appended
    )

# Company
class CompanyListView(generic.ListView):
    model = Company
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.all().order_by('company_name')

class CompanyDetailView(generic.DetailView):
    model = Company

class CompanyCreate(CreateView):
    model = Company
    fields = '__all__'

class CompanyUpdate(UpdateView):
    model = Company
    fields = '__all__'

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('index')



# Branch
class BranchListView(generic.ListView):
    model = Branch
    paginate_by = 50

    def get_queryset(self):
        return Branch.objects.all().order_by('branch_name')

class BranchDetailView(generic.DetailView):
    model = Branch


class BranchCreate(CreateView):
    model = Branch
    fields = '__all__'

class BranchUpdate(UpdateView):
    model = Branch
    fields = '__all__'

class BranchDelete(DeleteView):
    model = Branch
    success_url = reverse_lazy('index')




# Customer
class CustomerListView(generic.ListView):
    model = Customer
    paginate_by = 200

    def get_queryset(self):
        return Customer.objects.all().order_by('customer_name')

class CustomerDetailView(generic.DetailView):
    model = Customer

# Occassion
class OccassionListView(generic.ListView):
    model = Occassion
    paginate_by = 200

    def get_queryset(self):
        return Occassion.objects.all().order_by('occassion_name')

class OccassionDetailView(generic.DetailView):
    model = Occassion

# Order
class OrderListView(generic.ListView):
    model = Order
    paginate_by = 200

    def get_queryset(self):
        return Order.objects.all().order_by('-Order_Date')

class OrderDetailView(generic.DetailView):
    model = Order


# FORMS HANDLING
def data_upload(request):
 
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            file = Document()
            file.name = form.cleaned_data['name']
            file.file = form.cleaned_data['file']
#            file.save()
            process_data(request.FILES['file'])
#            handle_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = DocumentForm()

    return render(request, 'celebration/file_upload.html', {'form': form})



def process_data(upfile):

    import pandas as pd

    xls = pd.read_excel(upfile)

    company_name = 'Misterbaker LLC'

    branch_alias_dict = {
        'KMA': 'Karama'
    }


    occassion_alias_dict = {
        'H/B': 'Birthday', 
        'HB': 'Birthday', 
        'hb': 'Birthday', 
        'ANN': 'Anniversary', 
        'ANNIV': 'Anniversary', 
        'ANNIV.': 'Anniversary',
        'ANNNI': 'Anniversary',
        'ANNIV.': 'Anniversary',
        'ANNIVERSARY': 'Anniversary',
        'B TRANS': 'Branch Transfer',
        'B.TRANS.': 'Branch Transfer',
        'B TRANSFER': 'Branch Transfer',
        'B. TRANSFER': 'Branch Transfer',
        'B.T': 'Branch Transfer',
        'B.TRANSFER': 'Branch Transfer',
        'B/TRANS': 'Branch Transfer',
        'BT': 'Branch Transfer',
    }

    col_name_map = {
        'Branch': 'Branch',
        'Order Date': 'Order_Date',
        'Delivery Date': 'Delivery_Date',
        'Customer Name': 'Customer_Name',
        'Order #': 'Order_No', 
        'Contact #': 'Contact_No', 
        'Total Amount': 'Total_Amount', 
        'Remarks': 'Occassion',
    }

    xls=xls.rename(columns=col_name_map, index=str)

    xls = xls[['Branch', 'Order_Date', 'Customer_Name', 'Order_No', 'Contact_No', 'Total_Amount', 'Occassion']]

    xls.dropna(subset=['Contact_No'], inplace=True)

    xls[['Order_Date']] = xls[['Order_Date']].apply(pd.to_datetime, errors='coerce')
    xls[['Order_No', 'Contact_No', 'Total_Amount',]] = xls[['Order_No', 'Contact_No', 'Total_Amount',]].apply(pd.to_numeric, errors='coerce')

    xls['Contact_No'] = xls['Contact_No'].fillna(0.0).astype(int)

    xls['Branch'] = xls['Branch'].replace(branch_alias_dict)
    xls['Occassion'] = xls['Occassion'].replace(occassion_alias_dict)

    dict_list = xls.to_dict('records')

    for i in dict_list:
        print ('$$%$%$%%&####### PARSING DICT ##################')
        try:
            # Create order 
            new_order, created = Order.objects.get_or_create(Order_No__exact=i['Order_No'])
            if created:
                print ('############# NEW ORDER ENTRY START ##################')
                new_order.Company, c0 = Company.objects.get_or_create(
                    company_name = company_name,
                )
                new_order.Order_No = i['Order_No']
                new_order.Order_Date = i['Order_Date']
                new_order.Total_Amount = i['Total_Amount']
                new_order.Customer, c1 = Customer.objects.get_or_create(
                                    phone_number = i['Contact_No'],
                                    customer_name = i['Customer_Name']
                                    )
                new_order.Occassion, c2 = Occassion.objects.get_or_create(occassion_name = i['Occassion'])
                new_order.Branch, c3 = Branch.objects.get_or_create(branch_name = i['Branch'], company_name = new_order.Company )

                new_order.save()
                print ('converted'+str(i))
            else:
                print ('entry already exists')
        except Exception as e:
            print ('error')
            print (e)



# USER PROFILE
from .models import Profile

class ProfileCreate(CreateView):
    model = Profile
    fields = '__all__'



from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import UserForm, ProfileForm


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('index')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'celebration/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })