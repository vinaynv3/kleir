from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from django.contrib import messages

#ListView
class ListCustomers(ListView):
    model = ClientInfo
    template_name = 'PropertyDocs/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_reference_details = {}
        customers = ClientInfo.objects.order_by('-Date_Time')[:5]
        for customer in customers:
            last_bank_valuation = customer.bankref_set.last()
            #print(customer.Firstname, last_bank_valuation.Reference_Number)
            try:
                customer_reference_details[customer] = last_bank_valuation.Reference_Number
            except AttributeError:
                customer.delete()

        context = {'customer_reference_details':customer_reference_details}
        return context



# DoesNotExist exception.


#DetailView
class CustomerDetails(LoginRequiredMixin,DetailView):

    model = ClientInfo
    template_name = 'PropertyDocs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banks = BankRef.objects.filter(client_info_id = self.kwargs.get('pk'))
        customer = ClientInfo.objects.get(pk=self.kwargs.get('pk'))
        context = {'customer':customer,'banks':banks}
        return context





#create customer view
class CreateCustomer(LoginRequiredMixin,CreateView):
    model = ClientInfo
    fields = ['Firstname','Lastname','Contact','Email']

    def form_valid(self, form):
        form.instance.Created_By = self.request.user
        return super(CreateCustomer, self).form_valid(form)
        #super().__init__(make, model, year) =>test


class AddBankRef(LoginRequiredMixin,CreateView):
    model = BankRef
    fields = ['Reference_Number','Bank_Type']


    def form_valid(self, form):
        form.instance.client_info_id = self.kwargs.get('pk')
        #customer = ClientInfo.objects.get(Client_ID = self.kwargs.get('pk'))
        #messages.success(request, f' Report created for {customer.Firstname}!')
        return super(AddBankRef, self).form_valid(form)
