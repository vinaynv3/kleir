from django.shortcuts import render

from PropertyDocs.models import *
from Technical.models import *
from ImageUpload.models import *
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.exceptions import ObjectDoesNotExist

from django.db import models

db_models = [Documents,Address,Insights,MarketingValue,Plan,LegalLandmarks,
            SiteVisitLandmarks,Photos,Maps,AsPerDocuments,AsPerPlan,
            Actuals,Deviations,PermissibleBUA,ActualBUA,SanctionedArea,
            AreaDetails,Rate,TotalValue,FairMarketValue,PropertyStatus,FinalNotes
            ]



class ViewerManager(models.Manager):

    def document(self,DocID = None):

        dataSet = []
        pos = 0
        lookup = True

        while pos < len(db_models) and lookup:
            try:
                object = db_models[pos].objects.get(connection_id = DocID)
                dataSet.append(object)
                pos +=1

            except ObjectDoesNotExist:
                lookup = False
                print("LookUp Failed")
                dataSet = []

        if dataSet != []:

            """
            bank = BankRef.objects.get(pk = DocID)
            customer = ClientInfo.objects.get(pk = bank.client_info_id)
            dataSet.insert(0,bank)
            dataSet.insert(0,customer)
            """

            return dataSet


class ViewInterface(BankRef):
    viewer = ViewerManager()

def doc_complete(bank_id):
    """
    Document completion status is in relation Data Entry team
    Note: Data entry team doesn't enter technical detail data
    """
    try:
        #Check in final model
        if FinalNotes.objects.get(connection_id=bank_id):
            return True
    except FinalNotes.DoesNotExist:
        return False


"""
Data representation & Manipulation classes
"""


class BFL_Urban:

    def __init__(self,data = None):
        self.data = data

    def clean(self):

        data = {}
        for obj in self.data:
            data[str(obj.__class__).split(".")[-1].split("'")[0]] = []

            for k,v in obj.__dict__.items():
                if (not k.startswith("_")) and k != "id" and k != "connection_id":
                        data[str(obj.__class__).split(".")[-1].split("'")[0]].append(v)
        return data




    def personalDetailsContainer(self):
        cell_points = [(4,3),(4,9),(5,9),(6,9),(6,3),(7,4),(8,3)]
        data = self.clean()
        profile_data = data['BankRef'][0] + data['Documents'][1:4]+data['ClientInfo'][3]+data['Documents'][4:]

def ViewDocument(request,*args,**kwargs):

    if doc_complete(kwargs['bank_id']):

        bankName = BankRef.objects.get(pk=kwargs['bank_id']).Bank_Type
        template_path = 'C:\Project\kleir\Viewer\data\ExcelFiles\{0}.xlsx'.format(bankName)
        path_to_pdf = r'C:\Project\kleir\Viewer\data\ExcelFiles\sample.pdf'

        with open(template_path,'rb') as xlsx:

            import win32com.client
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            wb = excel.Workbooks.Open(template_path)

            work_sheets = wb.Worksheets[0]

            ws_index_list = [1,4,5] #say you want to print these sheets
            #wb.WorkSheets(ws_index_list).Select()
            work_sheets.ExportAsFixedFormat(0, path_to_pdf)
            excel.Application.Quit()


        with open(path_to_pdf,'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response

    else:
        return HttpResponse("Document is In-complete")
