from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PropertyDocs.models import *
from django.views import View
from .BusinessLogicAlgo.doc_navigator import *


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
