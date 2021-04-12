from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from Technical.models import *
from django.views import View
from .BusinessLogicAlgo.doc_navigator import *
from django.core.exceptions import ObjectDoesNotExist


"""
Direction View
"""

class DirectionView:

    def re_direct(request,*args,**kwargs):

        bankid = kwargs['bank_id']
        obj = Direction()
        url_namespace = obj.get_url_namespace(bankid)


        if obj.doc_complete(bankid):
            return HttpResponseRedirect(reverse(url_namespace, kwargs={'slug': kwargs['slug'],
            'pk':kwargs['pk'], 'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))
        else:
            return HttpResponseRedirect(reverse(url_namespace, kwargs={'slug': kwargs['slug'],
            'pk':kwargs['pk'], 'bank_type':kwargs['bank_type'],'bank_id':kwargs['bank_id']}))

class Collections(View):

    template_name = 'PropertyDocs/doc_collections_main.html'

    def get(self, request, *args, **kwargs):
        obj = Collection()
        docs = obj.get_model_objects(self.kwargs.get('bank_id'))

        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk=self.kwargs.get('pk'))

        return render(request, self.template_name, {'documents': docs,'bank':bank,'customer':customer})

class ViewBankDetails(View):
    template_name = 'PropertyDocs/view.html'

    def get(self, request, *args, **kwargs):

        bank = get_object_or_404(BankRef,pk = self.kwargs.get('bank_id'))
        customer = get_object_or_404(ClientInfo,pk=self.kwargs.get('pk'))

        return render(request, self.template_name, {'bank':bank,'customer':customer})

def SearchView(request,*args,**kwargs):
    search_post = request.GET.get('RefNo')
    search_post = search_post.strip() #strip space

    if len(search_post) == 0:
        current_url_path = request.headers.get('Referer')
        return HttpResponseRedirect(current_url_path)

    bank_record_update = {}
    position = 0
    try:
        bank = BankRef.objects.get(Reference_Number = search_post)
        if FinalNotes.objects.get(connection_id=bank.id):
            bank_record_update[position]=True
    except ObjectDoesNotExist:
        bank_record_update[position]=False


    if search_post:

        try:
            bank = BankRef.objects.get(Reference_Number = search_post)
            customer = ClientInfo.objects.get(pk=bank.client_info_id)
            return render(request,'PropertyDocs/search-result.html' , {'bank':bank,'customer':customer,'bank_record_update':bank_record_update})

        except ObjectDoesNotExist:
            messages.info(request, 'Invalid Reference Number, please enter valid RefNo')
            current_url_path = request.headers.get('Referer')
            return HttpResponseRedirect(current_url_path)


def about(request,*args,**kwargs):

    if request.method == 'GET':
        return render(request,'PropertyDocs/about.html' , {})
