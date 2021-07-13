from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .forms import *
from django.views import View
from django.contrib import messages
from PropertyDocs.models import *
from .models import *

"""
Technical models - Form control algorithm
"""
#models
database_models = [Actuals,SanctionedArea,FairMarketValue,FinalNotes]
#model relative url namespaces
model_urls = ['technical-layout','technical-BUA','technical-PropertyValue','technical-FairMarket','update-templates']

class TechnicalModelsPosition:

    #function returns current data entry url position
    def get_url_namespace(self,bank_id):
        doc_results = self.get_current_model_value(bank_id)
        return doc_results[1]

    # function returns current property documents position
    def get_current_model_value(self,bank_id):
        """
        Check BankRef model pk in between models Documents and SiteVisitLandmarks
        """
        current_id = bank_id
        model_position = 0
        status = False
        url_namespace = None

        while model_position < len(database_models) and not status:
            try:
                if database_models[model_position].objects.get(connection_id=current_id):
                    model_position +=1
            except database_models[model_position].DoesNotExist:
                status = True

        if model_position == len(database_models):
            url_namespace = model_urls[model_position]
        else:
            url_namespace = model_urls[model_position]

        return [ model_position, url_namespace ]

    def doc_complete(self, bank_id):
        """
        Document completion status is in relation Technical team
        Note: Data entry team doesn't enter technical detail data
        """
        try:
            #Check in final model
            if FinalNotes.objects.get(connection_id=bank_id):
                return True
        except FinalNotes.DoesNotExist:
            return False

"""
Finds current position of document
example: if there are 3 pages, let say page 1 is completed, the current position is page 2
"""
@login_required
def Position(request,*args,**kwargs):

    bankid = kwargs['bank_id']
    obj = TechnicalModelsPosition()
    url_namespace = obj.get_url_namespace(bankid)


    if obj.doc_complete(bankid):
        return HttpResponseRedirect(reverse(url_namespace, kwargs={'slug': kwargs['slug'],
            'pk':kwargs['pk'], 'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
    else:
        return HttpResponseRedirect(reverse(url_namespace, kwargs={'slug': kwargs['slug'],
            'pk':kwargs['pk'], 'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

"""
Technical detail models collection suite
"""
class TechnicalCollections(View):

    template_name = 'Technical/technical_collections.html'

    def get(self, request, *args, **kwargs):

        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk=self.kwargs.get('pk'))

        return render(request, self.template_name, {'bank':bank,'customer':customer})


"""
Technical layout details: CREATE
"""
@login_required
def LayoutView(request,*args,**kwargs):

    if request.method == 'POST':

        split_request_data = [ chunk for chunk in request.POST.lists()]
        import collections
        filter_key = collections.OrderedDict(split_request_data)
        position = list(filter_key.keys()).index('East_to_west_in_Feet')

        details = dict(split_request_data[position:])

        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        docs_data = dict(zip(keys,list(values[0:,0])))
        plan_data = dict(zip(keys,list(values[0:,1])))
        actual_data = dict(zip(keys,list(values[0:,2])))

        layout = LayoutForm(request.POST)
        docs = DocsForm(docs_data)
        plan = PlanForm(plan_data)
        actuals = ActualsForm(actual_data)

        if docs.is_valid() and layout.is_valid() and plan.is_valid() and actuals.is_valid():
            try:
                layout = layout.save(commit=False)
                layout.connection_id = kwargs['bank_id']
                layout.save()

                docs = docs.save(commit=False)
                docs.connection_id = kwargs['bank_id']
                docs.save()

                plan = plan.save(commit=False)
                plan.connection_id = kwargs['bank_id']
                plan.save()

                actuals = actuals.save(commit=False)
                actuals.connection_id = kwargs['bank_id']
                actuals.save()

                messages.success(request, 'Property Layout details added successfully')
                return HttpResponseRedirect(reverse('technical-BUA',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
            except IntegrityError:
                messages.success(request, 'Property Layout details added successfully')
                return HttpResponseRedirect(reverse('technical-BUA',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')
    else:

        layout = LayoutForm()
        docs = DocsForm()
        plan = PlanForm()
        actuals = ActualsForm()
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request,'Technical/docs.html', {'form1':docs,'form2':layout, 'form3':plan,'form4':actuals,'bank':bank,'customer':customer})


"""
Technical layout details: UPDATE
"""
@login_required
def LayoutViewUpdate(request, *args,**kwargs):

    layout_instance = get_object_or_404(Layout,connection_id = kwargs['bank_id'])
    docs_instance = get_object_or_404(AsPerDocuments,connection_id = kwargs['bank_id'])
    plan_instance = get_object_or_404(AsPerPlan,connection_id = kwargs['bank_id'])
    actual_instance = get_object_or_404(Actuals,connection_id = kwargs['bank_id'])


    if request.method == 'POST':

        split_request_data = [ chunk for chunk in request.POST.lists()]
        import collections
        filter_key = collections.OrderedDict(split_request_data)
        position = list(filter_key.keys()).index('East_to_west_in_Feet')


        details = dict(split_request_data[position:])

        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        docs_data = dict(zip(keys,list(values[0:,0])))
        plan_data = dict(zip(keys,list(values[0:,1])))
        actual_data = dict(zip(keys,list(values[0:,2])))

        layout = LayoutForm(request.POST, instance = layout_instance)
        docs = DocsForm(docs_data, instance = docs_instance)
        plan = PlanForm(plan_data, instance = plan_instance)
        actuals = ActualsForm(actual_data, instance = actual_instance)

        if docs.is_valid() and layout.is_valid() and plan.is_valid() and actuals.is_valid():
            try:
                layout = layout.save(commit=False)
                layout.connection_id = kwargs['bank_id']
                layout.save()

                docs = docs.save(commit=False)
                docs.connection_id = kwargs['bank_id']
                docs.save()

                plan = plan.save(commit=False)
                plan.connection_id = kwargs['bank_id']
                plan.save()

                actuals = actuals.save(commit=False)
                actuals.connection_id = kwargs['bank_id']
                actuals.save()

                messages.info(request, 'Property Layout details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
            except IntegrityError:
                messages.info(request, 'Property Layout details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')
    else:

        layout = LayoutForm(instance = layout_instance)
        docs = DocsForm(instance = docs_instance)
        plan = PlanForm(instance = plan_instance)
        actuals = ActualsForm(instance = actual_instance)
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        document ="Update -FLAG"
        return render(request,'Technical/docs.html', {'form1':docs,'form2':layout, 'form3':plan,'form4':actuals,'bank':bank,'customer':customer,'document':document})

"""
BUA - Create
"""
@login_required
def BUA_View(request,*args,**kwargs):

    if request.method == 'POST':
        split_request_data = [ chunk for chunk in request.POST.lists()]

        import collections
        filter_key = collections.OrderedDict(split_request_data)
        position = list(filter_key.keys()).index('Basement_Stilt_area')
        details = dict(split_request_data[position:])
        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        permissible_data = dict(zip(keys,list(values[0:,0])))
        actual_data = dict(zip(keys,list(values[0:,1])))
        sanctioned_data = dict(zip(keys,list(values[0:,2])))

        deviations = DeviationsForm(request.POST)
        permissible = PermissibleBUAForm(permissible_data)
        actual = ActualBUAForm(actual_data)
        sanctioned = SanctionedAreaForm(sanctioned_data)


        if deviations.is_valid() and permissible.is_valid() and actual.is_valid() and sanctioned.is_valid():
            try:
                deviations = deviations.save(commit=False)
                deviations.connection_id = kwargs['bank_id']
                deviations.save()

                permissible = permissible.save(commit=False)
                permissible.connection_id = kwargs['bank_id']
                permissible.save()

                actual = actual.save(commit=False)
                actual.connection_id = kwargs['bank_id']
                actual.save()

                sanctioned = sanctioned.save(commit=False)
                sanctioned.connection_id = kwargs['bank_id']
                sanctioned.save()

                messages.success(request, 'Property BUA details added successfully')
                return HttpResponseRedirect(reverse('technical-PropertyValue',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
            except IntegrityError:
                messages.success(request, 'Property BUA details added successfully')
                return HttpResponseRedirect(reverse('technical-PropertyValue',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')


    else:
        deviations = DeviationsForm()
        permissible = PermissibleBUAForm()
        actual = ActualBUAForm()
        sanctioned = SanctionedAreaForm()
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request,'Technical/BUA.html', {'form1':deviations,'form2':permissible, 'form3':actual,'form4':sanctioned,'bank':bank,'customer':customer})


"""
BUA - Update
"""
@login_required
def BUA_View_Update(request,*args,**kwargs):

    deviations_instance = get_object_or_404(Deviations,connection_id = kwargs['bank_id'])
    permissible_instance = get_object_or_404(PermissibleBUA,connection_id = kwargs['bank_id'])
    actual_instance = get_object_or_404(ActualBUA,connection_id = kwargs['bank_id'])
    sanctioned_instance = get_object_or_404(SanctionedArea,connection_id = kwargs['bank_id'])

    if request.method == 'POST':
        split_request_data = [ chunk for chunk in request.POST.lists()]

        import collections
        filter_key = collections.OrderedDict(split_request_data)
        position = list(filter_key.keys()).index('Basement_Stilt_area')

        details = dict(split_request_data[position:])

        print(details)
        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        #print(values, values.shape, values.size)

        permissible_data = dict(zip(keys,list(values[0:,0])))
        actual_data = dict(zip(keys,list(values[0:,1])))
        sanctioned_data = dict(zip(keys,list(values[0:,2])))

        #print(permissible,'\n',actual,'\n',sanctioned)
        deviations = DeviationsForm(request.POST,instance = deviations_instance)
        permissible = PermissibleBUAForm(permissible_data,instance = permissible_instance)
        actual = ActualBUAForm(actual_data,instance = actual_instance)
        sanctioned = SanctionedAreaForm(sanctioned_data, instance = sanctioned_instance)


        if deviations.is_valid() and permissible.is_valid() and actual.is_valid() and sanctioned.is_valid():
            try:
                deviations = deviations.save(commit=False)
                deviations.connection_id = kwargs['bank_id']
                deviations.save()

                permissible = permissible.save(commit=False)
                permissible.connection_id = kwargs['bank_id']
                permissible.save()

                actual = actual.save(commit=False)
                actual.connection_id = kwargs['bank_id']
                actual.save()

                sanctioned = sanctioned.save(commit=False)
                sanctioned.connection_id = kwargs['bank_id']
                sanctioned.save()

                messages.info(request, 'Property BUA details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
            except IntegrityError:
                messages.info(request, 'Property BUA details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')


    else:
        deviations = DeviationsForm(instance = deviations_instance)
        permissible = PermissibleBUAForm(instance = permissible_instance)
        actual = ActualBUAForm(instance = actual_instance)
        sanctioned = SanctionedAreaForm(instance = sanctioned_instance)
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        document ="Update -FLAG"
        return render(request,'Technical/BUA.html', {'form1':deviations,'form2':permissible, 'form3':actual,'form4':sanctioned,'bank':bank,'customer':customer,'document':document})


"""
PropertyValue - Create
"""
@login_required
def PropertyValueView(request,*args,**kwargs):

    if request.method == 'POST':
        split_request_data = [ chunk for chunk in request.POST.lists()]

        import collections
        filter_key = collections.OrderedDict(split_request_data)
        start = list(filter_key.keys()).index('Land_area')
        end = list(filter_key.keys()).index('Car_park')



        details = dict(split_request_data[start:end+1])
        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        area_data = dict(zip(keys,list(values[0:,0])))
        rate_data = dict(zip(keys,list(values[0:,1])))
        total_data = dict(zip(keys,list(values[0:,2])))

        print(area_data, rate_data,total_data)

        fair_market_pos = list(filter_key.keys()).index('completion')
        fair_market_data = dict(split_request_data[fair_market_pos:])

        clean_fair_market_data_values = [ val[0] for val in fair_market_data.values()]
        fair_market_data = dict(zip(fair_market_data.keys(), clean_fair_market_data_values))
        print(fair_market_data)


        property = PropertyStatusForm(request.POST)
        area = AreaDetailsForm(area_data)
        rate = RateForm(rate_data)
        total = TotalValueForm(total_data)
        fair_market = FairMarketValueForm(fair_market_data)

        l = [property.is_valid() ,area.is_valid() , rate.is_valid() ,total.is_valid(),fair_market.is_valid()]
        print(l)

        if property.is_valid() and area.is_valid() and rate.is_valid() and total.is_valid() and fair_market.is_valid():

            try:
                property = property.save(commit=False)
                property.connection_id = kwargs['bank_id']
                property.save()

                area = area.save(commit=False)
                area.connection_id = kwargs['bank_id']
                area.save()

                rate = rate.save(commit=False)
                rate.connection_id = kwargs['bank_id']
                rate.save()

                total = total.save(commit=False)
                total.connection_id = kwargs['bank_id']
                total.save()

                fair_market = fair_market.save(commit=False)
                fair_market.connection_id = kwargs['bank_id']
                fair_market.save()

                messages.success(request, 'Property value details added successfully')
                return HttpResponseRedirect(reverse('technical-FairMarket',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

            except IntegrityError:
                messages.success(request, 'Property value details added successfully')
                return HttpResponseRedirect(reverse('technical-FairMarket',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')


    else:
        property = PropertyStatusForm()
        area = AreaDetailsForm()
        rate = RateForm()
        total = TotalValueForm()
        fair_market = FairMarketValueForm()
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        return render(request,'Technical/PropertyValue.html',{'property_value_form':property,'form1':area, 'form2':rate,'form3':total,'fair_market_form':fair_market,'bank':bank,'customer':customer})

"""
PropertyValue - Update
"""
@login_required
def PropertyValueViewUpdate(request,*args,**kwargs):

    property_instance = get_object_or_404(PropertyStatus,connection_id = kwargs['bank_id'])
    area_instance = get_object_or_404(AreaDetails,connection_id = kwargs['bank_id'])
    rate_instance = get_object_or_404(Rate,connection_id = kwargs['bank_id'])
    total_instance = get_object_or_404(TotalValue,connection_id = kwargs['bank_id'])
    fair_market_instance = get_object_or_404(FairMarketValue,connection_id = kwargs['bank_id'])

    if request.method == 'POST':
        split_request_data = [ chunk for chunk in request.POST.lists()]

        import collections
        filter_key = collections.OrderedDict(split_request_data)
        start = list(filter_key.keys()).index('Land_area')
        end = list(filter_key.keys()).index('Car_park')



        details = dict(split_request_data[start:end+1])
        keys = list(details.keys())
        value_list = list(details.values())

        import numpy as np
        values = np.array(value_list)

        area_data = dict(zip(keys,list(values[0:,0])))
        rate_data = dict(zip(keys,list(values[0:,1])))
        total_data = dict(zip(keys,list(values[0:,2])))

        fair_market_pos = list(filter_key.keys()).index('completion')
        fair_market_data = dict(split_request_data[fair_market_pos:])

        clean_fair_market_data_values = [ val[0] for val in fair_market_data.values()]
        fair_market_data = dict(zip(fair_market_data.keys(), clean_fair_market_data_values))


        property = PropertyStatusForm(request.POST, instance = property_instance)
        area = AreaDetailsForm(area_data,instance = area_instance)
        rate = RateForm(rate_data, instance = rate_instance)
        total = TotalValueForm(total_data, instance = total_instance)
        fair_market = FairMarketValueForm(fair_market_data, instance = fair_market_instance)

        if property.is_valid() and area.is_valid() and rate.is_valid() and total.is_valid() and fair_market.is_valid():

            try:
                property = property.save(commit=False)
                property.connection_id = kwargs['bank_id']
                property.save()

                area = area.save(commit=False)
                area.connection_id = kwargs['bank_id']
                area.save()

                rate = rate.save(commit=False)
                rate.connection_id = kwargs['bank_id']
                rate.save()

                total = total.save(commit=False)
                total.connection_id = kwargs['bank_id']
                total.save()

                fair_market = fair_market.save(commit=False)
                fair_market.connection_id = kwargs['bank_id']
                fair_market.save()

                messages.info(request, 'Property value details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
            except IntegrityError:
                messages.info(request, 'Property value details updated successfully')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
        else:
            messages.error(request, 'Oops!! Something went wrong, please try again.')


    else:
        property = PropertyStatusForm(instance = property_instance)
        area = AreaDetailsForm(instance = area_instance)
        rate = RateForm(instance = rate_instance)
        total = TotalValueForm(instance = total_instance)
        fair_market = FairMarketValueForm(instance = fair_market_instance)
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        document ="Update -FLAG"
        return render(request,'Technical/PropertyValue.html',{'property_value_form':property,'form1':area, 'form2':rate,'form3':total,'fair_market_form':fair_market,'bank':bank,'customer':customer,'document':document})



"""
FinalNotes - Create
"""
@login_required
def FinalNotesView(request,*args,**kwargs):
    if request.method == 'POST':
        final_notes = FinalForm(request.POST)

        if final_notes.is_valid():
            try:
                final_notes = final_notes.save(commit=False)
                final_notes.connection_id = kwargs['bank_id']
                final_notes.save()

                messages.success(request, 'Document is completed!')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

            except IntegrityError:
                messages.success(request, 'Document is completed!')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

    else:

        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        form = FinalForm()
        return render(request,'Technical/FinalForm.html',{'form':form,'bank':bank,'customer':customer})

"""
FinalNotes - Update
"""
@login_required
def FinalNotesViewUpdate(request,*args,**kwargs):

    notes_instance = get_object_or_404(FinalNotes,connection_id = kwargs['bank_id'])
    if request.method == 'POST':
        final_notes = FinalForm(request.POST, instance = notes_instance)

        if final_notes.is_valid():
            try:
                final_notes = final_notes.save(commit=False)
                final_notes.connection_id = kwargs['bank_id']
                final_notes.save()

                messages.info(request, 'Property Notes is updated')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

            except IntegrityError:
                messages.info(request, 'Property Notes is updated')
                return HttpResponseRedirect(reverse('update-templates',kwargs={'slug': kwargs['slug'],'pk':kwargs['pk'],
                                                    'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

    else:

        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        form = FinalForm(instance = notes_instance)
        document ="Update -FLAG"
        return render(request,'Technical/FinalForm.html',{'form':form,'bank':bank,'customer':customer,'document':document})
