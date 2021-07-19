
import os
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
from django.contrib import messages
import time

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
    Document complete status
    """
    try:
        #Check in final model
        if FinalNotes.objects.get(connection_id=bank_id):
            return True
    except FinalNotes.DoesNotExist:
        return False



def addPropertyDataToExcel(file_object):
    Lender = None
    t1 = time.time()
    if str(file_object[1]) == 'BFL':
        Lender = 'BFL.xlsx'

        xlsx_doc = BFL_Urban(data = file_object)
        xlsx_doc.cleanData()
        xlsx_doc.personalDetailsContainer()
        xlsx_doc.UpdateLocation()
        xlsx_doc.UpdatePropertyDesign()
        xlsx_doc.VerifyDocs()
        xlsx_doc.UpdatePropertyPlan()

    elif str(file_object[1]) == 'ABHFL':
        Lender = 'ABHFL.xlsx'

        xlsx_doc = ABHFL(data = file_object)
        xlsx_doc.cleanData()
        xlsx_doc.personalDetailsContainer()

    elif str(file_object[1]) == 'L&T':
        Lender = 'LT.xlsx'

        xlsx_doc = LT(data = file_object)
        xlsx_doc.cleanData()
        xlsx_doc.personalDetailsContainer()
        xlsx_doc.VerifyDocs()
    t2 = time.time()
    print('Excel processing time',t2-t1,' m_sec')
    return Lender


def changeDirHeroku():

    # file operations are done in below dir
    cwd = r'/app/staticfiles/DocCreation'
    if os.getcwd() == cwd:
        return True
    else:
        path = os.getcwd()+r'/staticfiles/DocCreation'
        os.chdir(path)
        if cwd == os.getcwd():
            return True
        else:
            return False

def changeDirLocal():

    cwd = r'C:\Project\kleir\staticfiles\DocCreation'
    if os.getcwd() == cwd:
        return True
    else:

        path = os.getcwd()+r'\\staticfiles\\DocCreation'
        os.chdir(path)
        print('path:',path,'dir',os.getcwd())
        if cwd == os.getcwd():
            return True
        else:
            return False

#PDF Viewer controller
@xframe_options_sameorigin
def ViewDocument(request,*args,**kwargs):

    if doc_complete(kwargs['bank_id']):


        file_object = ViewInterface.viewer.document(DocID = kwargs['bank_id'])
        financier = None

        if os.name == 'posix':
            financier = addPropertyDataToExcel(file_object)

        """
        # UNIX (Linux-posix os)
        #print('cloud:',changeDirHeroku())
        if os.name == 'posix':
            if changeDirHeroku():
                financier = addPropertyDataToExcel(file_object)
        # windows os
        if os.name == 'nt':
            if changeDirLocal():
                financier = addPropertyDataToExcel(file_object)
        """


        import requests
        import base64
        import json

        excel_base64_data = None

        x1 = time.time()

        with open(financier,'rb') as excel:
            read_excel_base64 = excel.read()
            encode_excel = base64.b64encode(read_excel_base64)
            excel_base64_data = encode_excel.decode('utf-8')

        pdf_token = None
        with open('pdf_api.txt') as f:
            pdf_token = f.read().strip()





        url = 'https://getoutpdf.com/api/convert/document-to-pdf'
        data = {
                "api_key": pdf_token,
                "document": excel_base64_data,
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print("API call iinititated")
        call_api_convertPdf = requests.post(url, data=json.dumps(data), headers=headers)
        print("Tokens left: ",call_api_convertPdf.json()['tokens_left'])

        pdf_base64_data = call_api_convertPdf.json()['pdf_base64']
        base64_img_bytes = pdf_base64_data.encode('utf-8')

        x2 = time.time()
        print('API processing time ',x2-x1,' m_sec')

        y1 = time.time()
        with open('PropertyValuation.pdf', 'wb') as pdf:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            pdf.write(decoded_image_data)
        y2 = time.time()
        print('PDF creation time ',y2-y1,' m_sec')

        bank = get_object_or_404(BankRef,pk = kwargs['bank_id'])
        customer = get_object_or_404(ClientInfo,pk = kwargs['pk'])

        context = {'bank':bank,'customer':customer,'path':None,'env':False}

        """
        #Heroku deployment settings
        if os.name == 'posix':
            context['env'] = True
        """
        return render(request,'Viewer/PDFviewer.html',context)

    else:
        messages.info(request, 'Property valuation details are incomplete, please complete the document')
        current_url_path = request.headers.get('Referer')
        return HttpResponseRedirect(current_url_path)
