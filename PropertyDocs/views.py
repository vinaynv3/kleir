from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist


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
        customer_list = []
        customers = ClientInfo.objects.order_by('-Date_Time')[:12]
        for customer in customers:
            last_bank_valuation = customer.bankref_set.last()
            try:
                customer_reference_details[customer] = last_bank_valuation
                customer_list.append({customer:last_bank_valuation})
            except AttributeError:
                customer.delete()

        context = {'customer_reference_details':customer_reference_details,'customer_list':customer_list}
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
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        return context

#Add Bank detauls
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

#Update Bank detauls
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

#Delete Bank details
class DeleteBankRef(LoginRequiredMixin,DeleteView):
    model = BankRef
    success_message = "Customer bank %(bank)s record removed successfully"

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

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, bank=self.object.Bank_Type)

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


"""
SiteVisit data business logic : create and update documents
"""

class AddLoanType(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Documents
    fields = ['SFDC_no','Product_Loan_Type','Person_met_at_site','Name_of_Applicant',
            'Name_of_Property_Owner_as_per_legal_document','Documents_Provided']
    success_message = "Customer bank Loan record %(loan)s added successfully"

    def form_valid(self, form):
        try:
            form.instance.connection_id = self.kwargs.get('bank_id')
            return super().form_valid(form)

        except IntegrityError:
            form.instance.connection_id = self.kwargs.get('bank_id')
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                kwargs.update({'instance': self.object})
        return kwargs


    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, loan=self.object.Product_Loan_Type,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddLoanType,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context :
            context['form'] = self.get_form()
        return context


class UpdateLoanType(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Documents
    fields = ['SFDC_no','Product_Loan_Type','Person_met_at_site','Name_of_Applicant',
            'Name_of_Property_Owner_as_per_legal_document','Documents_Provided']
    success_message = "Customer bank Loan record %(loan)s updated successfully"


    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, loan=self.object.Product_Loan_Type,)

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing bank_id & bank_type URL keys
        """
        document_record = get_object_or_404(Documents,pk = self.kwargs.get('doc_id'))
        return document_record

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateLoanType,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank,'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddAddress(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Address
    fields = ['Postal_address_of_the_property','Legal_address_of_the_property',
            'Landmark_nearby','Lat_and_Long','Distance_from_City_Centre']
    success_message = "Customer property %(address)s added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddAddress, self).form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, address=self.object.Postal_address_of_the_property,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddAddress,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

class UpdateAddress(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Address
    fields = ['Postal_address_of_the_property','Legal_address_of_the_property',
            'Landmark_nearby','Lat_and_Long','Distance_from_City_Centre']
    success_message = "Customer property %(address)s updated successfully"

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing bank_id & bank_type URL keys
        """
        document_record = get_object_or_404(Address, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, address=self.object.Postal_address_of_the_property,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateAddress,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddInsights(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = Insights
    fields = ['Property_holding_type','Type_of_the_property',
            'Approved_usage','Actual_usage','Current_Zoning_as_per_CDP','Occupancy_details_floorwise']
    success_message = "Customer property type %(property_type)s added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddInsights, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs


    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, property_type=self.object.Type_of_the_property,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddInsights,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class UpdateInsights(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    model = Insights
    fields = ['Property_holding_type','Type_of_the_property',
            'Approved_usage','Actual_usage','Current_Zoning_as_per_CDP','Occupancy_details_floorwise']
    success_message = "Customer property type %(property_type)s added successfully"

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing property Insights URL keys
        """
        document_record = get_object_or_404(Insights, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, property_type=self.object.Type_of_the_property,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateInsights,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddMarketingValue(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = MarketingValue
    fields = ['Address_Matching','Local_Municipal_body',
            'Marketability','Boundaries_matching','Property_Identified']
    success_message = "Customer property jurisdiction  %(jurisdiction)s added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddMarketingValue, self).form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs


    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, jurisdiction=self.object.Local_Municipal_body,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddMarketingValue,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class UpdateMarketingValue(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    model = MarketingValue
    fields = ['Address_Matching','Local_Municipal_body',
            'Marketability','Boundaries_matching','Property_Identified']
    success_message = "Customer property jurisdiction  %(jurisdiction)s updated successfully"


    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing property Insights URL keys
        """
        document_record = get_object_or_404(MarketingValue, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        """
        cleaned_data is the cleaned data from the form which is used for string formatting
        """
        return self.success_message % dict(cleaned_data, jurisdiction=self.object.Local_Municipal_body,)

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateMarketingValue,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddAptPlan(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = Plan
    fields = ['Layout_plan_details','Approving_authority',
            'Construction_plan_details','Plan_validity_from','To_date']
    success_message = "Customer property plan details added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddAptPlan, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs

    def get_success_message(self, *args,**kwrgs):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddAptPlan,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class UpdateAptPlan(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    model = Plan
    fields = ['Layout_plan_details','Approving_authority',
            'Construction_plan_details','Plan_validity_from','To_date']
    success_message = "Customer property plan details added successfully"



    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing property Insights URL keys
        """
        document_record = get_object_or_404(Plan, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateAptPlan,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddLegalLandmarks(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = LegalLandmarks
    fields = ['East','West','North','South']
    success_message = "Customer property legal landmark details added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddLegalLandmarks, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs

    def get_success_message(self, *args,**kwrgs):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddLegalLandmarks,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class UpdateLegalLandmarks(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    model = LegalLandmarks
    fields = ['East','West','North','South']
    success_message = "Customer property legal landmark details added successfully"

    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing property Insights URL keys
        """
        document_record = get_object_or_404(LegalLandmarks, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateLegalLandmarks,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})


class AddSiteVisitLandmarks(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = SiteVisitLandmarks
    fields = ['East','West','North','South']
    success_message = "Customer property site visit landmark details added successfully"

    def form_valid(self, form):
        form.instance.connection_id = self.kwargs.get('bank_id')
        return super(AddSiteVisitLandmarks, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            try:
                object = self.model.objects.get(connection_id = self.kwargs.get('bank_id'))
                kwargs.update({'instance': object})
            except ObjectDoesNotExist:
                print("test=self.object")
                kwargs.update({'instance': self.object})
        return kwargs



    def get_success_message(self, *args,**kwrgs):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(AddSiteVisitLandmarks,self).get_context_data(**kwargs)
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context['customer'] = customer
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class UpdateSiteVisitLandmarks(LoginRequiredMixin,SuccessMessageMixin,UpdateView):

    model = SiteVisitLandmarks
    fields = ['East','West','North','South']
    success_message = "Customer property site visit landmark details added successfully"


    def get_object(self,*args,**kwargs):
        """
        accessing record from db by passing property Insights URL keys
        """
        document_record = get_object_or_404(SiteVisitLandmarks, pk = self.kwargs.get('doc_id'))
        return document_record

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self,**kwargs):
        """
        FormMixin: insert customer info and BankRef model form into context data
        """
        context = super(UpdateSiteVisitLandmarks,self).get_context_data(**kwargs)
        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk = self.kwargs.get('pk'))
        context = {'customer':customer,'bank':bank, 'document':self.get_object()}
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('doc-collections', kwargs={'slug':self.kwargs.get('slug'),'pk': self.kwargs.get('pk'),
                            'bank_type':self.kwargs.get('bank_type'),'bank_id':self.kwargs.get('bank_id')})
