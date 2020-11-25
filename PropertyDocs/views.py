from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from django.contrib.messages.views import SuccessMessageMixin

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
class UpdateCustomer(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    """
    View updates customer information
    """
    model = ClientInfo
    fields = ['Firstname','Lastname','Contact','Email']
    success_message = "Customer record %(customer)s was updated successfully"

    def form_valid(self, form):
        """
        Update customer record editor information
        """
        form.instance.Created_By = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, customer=self.object.Firstname,)

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

#Delete customer information
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


class AddBankRef(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = BankRef
    fields = ['Reference_Number','Bank_Type']
    success_message = "Bank record %(bank)s was added successfully"


    def form_valid(self, form):
        form.instance.client_info_id = self.kwargs.get('pk')
        return super(AddBankRef, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, bank=self.object.Bank_Type,)

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

class UpdateBankRef(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = BankRef
    fields = ['Reference_Number','Bank_Type']
    success_message = "Bank record %(bank)s was updated successfully"


    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, bank=self.object.Bank_Type,)

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing bank_id & bank_type URL keys
        """
        bank_record = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        return bank_record

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateBankRef,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

class DeleteBankRef(LoginRequiredMixin,DeleteView):
    model = BankRef

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing bank_id & bank_type URL keys
        """
        bank_record = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        return bank_record

    def get_context_data(self,**kwargs):
        """
        Display customers all property loan records
        """
        context = super().get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk=self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank}
        return context

    def get_success_url(self,*args,**kwargs):
        return reverse('Detail-Page',kwargs = {'slug':self.kwargs.get('slug'),
                           'pk':self.kwargs.get('pk')})

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
