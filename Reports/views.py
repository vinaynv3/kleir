from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import ClientInfo, BankRef
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from Technical.models import *

"""
Utility Class for BankRef & ClientInfo Model
"""
class DisplayDetails:

    def __init__(self):
        self.bank = None
        self.date = None
        self.ref = None
        self.slug = None
        self.ids = None

    def create(self,Bankobject):
        customer = ClientInfo.objects.get(pk=Bankobject.client_info_id)
        self.bank,self.date,self.ref  = Bankobject.Bank_Type, Bankobject.Date, Bankobject.Reference_Number
        self.ids = [customer.Client_ID,Bankobject.id,]
        self.slug = customer.Slug
        return self



# Create your views here.
@login_required
def ReportsHomeView(request,*args,**kwargs):
    return render(request,'Reports/multi_filter_search.html')

def getObjects(data):

    if len(data) == 3:

        if data['bank'] == 'ALL':
            bank_reports = BankRef.objects.filter(Date__gte =  data['fromDate']).filter( Date__lte= data['toDate'])
            return bank_reports

        else:
            bank_reports = BankRef.objects.filter(Date__gte =  data['fromDate']).filter( Date__lte= data['toDate']).filter(Bank_Type = data['bank'])
            return bank_reports

    elif len(data) == 2:
        if data['bank'] == 'ALL':
            date = list(data.keys())[1]
            bank_reports = BankRef.objects.filter(Date =  data[date])
            return bank_reports
        else:
            date = list(data.keys())[1]
            bank_reports = BankRef.objects.filter(Date =  data[date]).filter( Bank_Type = data['bank'])
            return bank_reports
    else:
        if data['bank'] == 'ALL':
            bank_reports = BankRef.objects.all()
            return bank_reports
        else:
            import datetime
            today = datetime.date.today()
            bank_reports = BankRef.objects.filter(Date =  today).filter( Bank_Type = data['bank'])
            return bank_reports

@login_required
def ReportsDispalyView(request,*args,**kwargs):
    page_no = kwargs['page']

    bank = request.GET.get('bank_type')
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')

    data = {'bank':request.GET.get('bank_type'),
            'fromDate' : request.GET.get('fromDate'),
            'toDate' : request.GET.get('toDate'),
            }

    data = {k: v for k, v in data.items() if v != ''}

    if not any([bank,fromDate,toDate]):
        url_path = request.headers.get('Referer')
        split_url = url_path.split("?")
        url = split_url[0][:-2]+str(page_no)+'/?'+split_url[1]
        return HttpResponseRedirect(url)


    if request.method == 'GET':
        Bankobjects = list(getObjects(data))
        utility_class_list = [ DisplayDetails() for i in range(len(Bankobjects))]
        report_display_list = [ utility_class_list[i].create(Bankobjects[i]) for i in range(len(Bankobjects))]
        pagerObject = Paginator(report_display_list,10)
        context = { 'objects':pagerObject.page(page_no), 'total_rows':len(report_display_list),'page_obj':pagerObject.page(page_no)}

        if len(report_display_list) == 0:
            messages.info(request, '0 records found')

        return render(request,'Reports/multi_filter_search.html',context)

@login_required
def ReportOptions(request,*args,**kwargs):

    bank_id = kwargs['bank_id']
    bank_record_update = {}
    position = 0
    try:
        if FinalNotes.objects.get(connection_id=bank_id):
            bank_record_update[position]=True
    except ObjectDoesNotExist:
        bank_record_update[position]=False


    try:
        bank = BankRef.objects.get(pk = bank_id)
        customer = ClientInfo.objects.get(pk=bank.client_info_id)
        return render(request,'Reports/home_loan.html' , {'bank':bank,'customer':customer,'bank_record_update':bank_record_update})

    except ObjectDoesNotExist:
            messages.info(request, 'Something went wrong, Try again!')
            current_url_path = request.headers.get('Referer')
            return HttpResponseRedirect(current_url_path)
