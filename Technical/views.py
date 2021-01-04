from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib import messages
from PropertyDocs.models import *
from .models import *


"""
Technical layout details: CREATE
"""
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

            return HttpResponse("Thanks")


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
def LayoutViewUpdate(request, *args,**kwargs):
    pass



def BUA_View(request,*args,**kwargs):

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
        sanctioned_data = dict(zip(keys,list(values[0:,2])))
        actual_data = dict(zip(keys,list(values[0:,1])))

        #print(permissible,'\n',actual,'\n',sanctioned)
        deviations = DeviationsForm(request.POST)
        permissible = PermissibleBUAForm(permissible_data)
        actual = ActualBUAForm(actual_data)
        sactioned = SanctionedAreaForm(sanctioned_data)


        if deviations.is_valid() and permissible.is_valid() and actual.is_valid() and sactioned.is_valid():

            deviations = deviations.save(commit=False)
            deviations.connection_id = kwargs['bank_id']
            deviations.save()

            permissible = permissible.save(commit=False)
            permissible.connection_id = kwargs['bank_id']
            permissible.save()

            actual = actual.save(commit=False)
            actual.connection_id = kwargs['bank_id']
            actual.save()

            sactioned = sactioned.save(commit=False)
            sactioned.connection_id = kwargs['bank_id']
            sactioned.save()

            return HttpResponse("Thanks")


    else:
        deviations = DeviationsForm()
        permissible = PermissibleBUAForm()
        actual = ActualBUAForm()
        sactioned = SanctionedAreaForm()
        return render(request,'Technical/BUA.html', {'form1':deviations,'form2':permissible, 'form3':actual,'form4':sactioned})


"""
PropertyValue
"""
def PropertyValueView(request,*args,**kwargs):
    if request.method == 'POST':
        return HttpResponse("Thanks")

    else:
        property = PropertyStatusForm()
        area = AreaDetailsForm()
        rate = RateForm()
        total = TotalValueForm()
        fair_market = FairMarketValueForm()
        return render(request,'Technical/PropertyValue.html',{'property_value_form':property,'form1':area, 'form2':rate,'form3':total,'fair_market_form':fair_market})



"""
FinalNotes
"""
def FinalNotesView(request,*args,**kwargs):
    if request.method == 'POST':
        return HttpResponse("Thanks")

    else:

        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        form = FinalForm()
        return render(request,'Technical/FinalForm.html',{'form':form,'bank':bank,'customer':customer})
