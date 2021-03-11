from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import ClientInfo, BankRef

# Create your views here.
def ReportsHomeView(request,*args,**kwargs):
    return render(request,'Reports/multi_filter_search.html')

def getObjects(data):

    if len(data) is 3:
        bank_reports = BankRef.objects.filter(Date__gte =  data['fromDate']).filter( Date__lte= data['toDate']).filter(Bank_Type = Data['bank'])
        return bank_reports

    elif len(data) is 2:
        date = list(data.keys())[1]
        bank_reports = BankRef.objects.filter(Date =  data[date]).filter( Bank_Type = data['bank'])
        return bank_reports

    else:
        import datetime
        today = datetime.date.today()
        bank_reports = BankRef.objects.filter(Date =  today).filter( Bank_Type = data['bank'])
        return bank_reports


def ReportsDispalyView(request,*args,**kwargs):
    bank = request.GET.get('bank_type')
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')

    data = {'bank':request.GET.get('bank_type'),
            'fromDate' : request.GET.get('fromDate'),
            'toDate' : request.GET.get('toDate'),
            }

    data = {k: v for k, v in data.items() if v != ''}

    if request.method == 'GET':

        print(bank,fromDate,toDate)
        return HttpResponse("Recieved")
