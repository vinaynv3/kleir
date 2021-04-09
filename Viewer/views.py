from django.shortcuts import render
from PropertyDocs.models import *
from Technical.models import *
from ImageUpload.models import *
from .BankExcelTemplates import *
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .BankExcelTemplates import *

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

def addPropertyDataToExcel(file_object):
        xlsx_doc = BFL_Urban(data = file_object)
        xlsx_doc.cleanData()
        xlsx_doc.personalDetailsContainer()
        xlsx_doc.UpdateLocation()
        xlsx_doc.UpdatePropertyDesign()
        xlsx_doc.VerifyDocs()
        xlsx_doc.UpdatePropertyPlan()

def changeDir():

    import os

    # file operations are done in below dir
    cwd = r'C:\Project\kleir\ImageUpload\media'

    if os.getcwd() == cwd:
        return True
    else:
        path = os.getcwd()+r'\\ImageUpload\\media'
        os.chdir(path)
        status = True if path == os.getcwd() else False
        return status

#PDF Viewer controller
@xframe_options_sameorigin
def ViewDocument(request,*args,**kwargs):

    if doc_complete(kwargs['bank_id']):

        file_object = ViewInterface.viewer.document(DocID = kwargs['bank_id'])


        if changeDir():
            addPropertyDataToExcel(file_object)
        """
        else:
            raise Exception
        """

        import requests
        import base64
        import json

        excel_base64_data = None
        with open('BFL.xlsx','rb') as excel:
            read_excel_base64 = excel.read()
            encode_excel = base64.b64encode(read_excel_base64)
            excel_base64_data = encode_excel.decode('utf-8')

        url = 'https://getoutpdf.com/api/convert/document-to-pdf'
        data = {
                "api_key": "32ffa3a2686cf2a8bc16d98541e9c2f0997de23636adc0d9df7b1b00b9da24b8",
                "document": excel_base64_data,
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        call_api_convertPdf = requests.post(url, data=json.dumps(data), headers=headers)
        #print(call_api_convertPdf.json())

        pdf_base64_data = call_api_convertPdf.json()['pdf_base64']
        base64_img_bytes = pdf_base64_data.encode('utf-8')

        with open('decoded_image.pdf', 'wb') as pdf:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            pdf.write(decoded_image_data)

        """
        with open('decoded_image.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response


        if request.method == 'GET':
        """
        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])
        context = {'bank':bank,'customer':customer,'path':'http://127.0.0.1:8000/ImageUpload/media/decoded_image.pdf'}
        return render(request,'Viewer/PDFviewer.html',context)

    else:
        return HttpResponse("Document is In-complete")
