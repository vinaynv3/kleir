from django.shortcuts import render

"""
from Technical.models import *
from ImageUpload.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.db import models

class ViewerManager(models.Manager):

    models = [Documents,Address,Insights,MarketingValue,Plan,LegalLandmarks,
                    SiteVisitLandmarks,Photos,Maps,AsPerDocuments,AsPerPlan,
                    Actuals,Deviations,PermissibleBUA,ActualBUA,SanctionedArea,
                    AreaDetails,Rate,TotalValue,FairMarketValue,PropertyStatus,FinalNotes
                    ]

    dataSet = []

    def document(self,DocID = None):
        pos = 0
        lookup = True
        while pos < len(models) and lookup:
            try:
                object = models[pos].objects.get(connection_id = DocID)
                dataSet.append(object)
                pos +=1

            except ObjectDoesNotExist:
                lookup = False
                messages.info(request, 'Document is incomplete, please fill all the details to view')
"""
