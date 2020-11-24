from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from django.contrib import messages

#ListView
class ListCustomers(ListView):
    """
    Display list of last ten customer account bank records
    """
    model = ClientInfo
    template_name = 'PropertyDocs/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_reference_details = {}
        customers = ClientInfo.objects.order_by('-Date_Time')[:10]
        for customer in customers:
            last_bank_valuation = customer.bankref_set.last()
            try:
                customer_reference_details[customer] = last_bank_valuation
            except AttributeError:
                customer.delete()

        context = {'customer_reference_details':customer_reference_details}
        return context


#DetailView
class CustomerDetails(LoginRequiredMixin,DetailView):

    model = ClientInfo
    template_name = 'PropertyDocs/detail.html'

    def get_context_data(self, **kwargs):
        """
        Display customers all property loan records
        """
        context = super().get_context_data(**kwargs)
        banks = BankRef.objects.filter(client_info_id = self.kwargs.get('pk'))
        customer = get_object_or_404(ClientInfo,pk=self.kwargs.get('pk'))
        context = {'customer':customer,'banks':banks}
        return context


#create a new customer record
class CreateCustomer(LoginRequiredMixin,CreateView):
    """
    Adding a new customer record
    """
    model = ClientInfo
    fields = ['Firstname','Lastname','Contact','Email']

    def form_valid(self, form):
        form.instance.Created_By = self.request.user
        return super().form_valid(form)


#update customer information
class UpdateCustomer(LoginRequiredMixin,UpdateView):

    """
    View updates customer information
    """
    model = ClientInfo
    fields = ['Firstname','Lastname','Contact','Email']

    def form_valid(self, form):
        """
        Update customer record editor information
        """
        form.instance.Created_By = self.request.user
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateCustomer,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('Detail-Page', kwargs={'slug':self.object.Slug,'pk': self.object.Client_ID})

class DeleteCustomer(LoginRequiredMixin,DeleteView):
    model = ClientInfo
    success_url = '/'

    def get_context_data(self,**kwargs):
        """
        context customer object
        """
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        return context




class AddBankRef(LoginRequiredMixin,CreateView):
    model = BankRef
    fields = ['Reference_Number','Bank_Type']


    def form_valid(self, form):
        form.instance.client_info_id = self.kwargs.get('pk')
        #customer = ClientInfo.objects.get(Client_ID = self.kwargs.get('pk'))
        #messages.success(request, f' Report created for {customer.Firstname}!')
        return super(AddBankRef, self).form_valid(form)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddBankRef,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context
