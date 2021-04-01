from __future__ import print_function
from django.shortcuts import render
from PropertyDocs.models import *
from Technical.models import *
from ImageUpload.models import *
from .BankExcelTemplates import *
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

            bank = BankRef.objects.get(pk = DocID)
            customer = ClientInfo.objects.get(pk = bank.client_info_id)
            dataSet.insert(0,bank)
            dataSet.insert(0,customer)
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



#PDF Viewer controller
def ViewDocument(request,*args,**kwargs):

    if doc_complete(kwargs['bank_id']):
        import openpyxl
        wb = openpyxl.Workbook('test.xlsx')
        wb.save('test.xlsx')
        load_workbook = openpyxl.load_workbook('test.xlsx')
        sheet = load_workbook.active
        sheet.title = "vinay"
        load_workbook.save('test.xlsx')

        import time
        import cloudmersive_convert_api_client
        from cloudmersive_convert_api_client.rest import ApiException
        from pprint import pprint
        # Configure API key authorization: Apikey
        configuration = cloudmersive_convert_api_client.Configuration()
        configuration.api_key['Apikey'] = '3eafe039-75ee-4cf3-8d7a-38df7c662748'
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['Apikey'] = 'Bearer'
        # create an instance of the API class
        api_instance = cloudmersive_convert_api_client.ConvertDocumentApi(cloudmersive_convert_api_client.ApiClient(configuration))
        input_file = 'test.xlsx' # file | Input file to perform the operation on.
        try:
            # Convert Document to PDF
            api_response = api_instance.convert_document_xlsx_to_pdf(input_file)
            api_response1 = api_instance.convert_document_xlsx_to_pdf_with_http_info(input_file)
            print(type(api_instance))
            pprint("pass")
            pprint(api_response)
            with open(api_response,'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                return response
        except ApiException as e:
            print('failed')
            print("Exception when calling ConvertDocumentApi->convert_document_autodetect_to_pdf: %s\n" % e)
    else:
        return HttpResponse("Document is In-complete")
