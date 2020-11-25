
from .models import *

#models
database_models = [Documents,Address,Insights,MarketingValue,Plan,LegalLandmarks,SiteVisitLandmarks]
#model relative url namespaces
model_urls = []


#'<slug:slug>/<int:pid>/<bank_name>/<int:bank_id>/landlord/'
class Direction:

    #get landlord name
    def get_landlord_name_id(self, landlord_id):
        landlord_name = landlord.objects.get(pk = landlord_id)
        return [landlord_name.slug, landlord_name.pk]

    #get landlord property Reference number
    def get_landlord_reference_num(self,bank_id):
        ref = landlord_bank.objects.get(pk = bank_id)
        return ref.Reference_Number

    #get bank name in relation landlord property
    def get_bank(self,bank_id):
        bank = landlord_bank.objects.get(pk = bank_id)
        return bank.Bank_type

    # function returns current property documents position
    def get_current_model_value(self,bank_id):

        current_id = bank_id
        model_position = 0
        status = False
        url_id = None

        while model_position < len(database_models) and not status:
            try:
                if database_models[model_position].objects.get(connection_id=current_id):
                    current_id = database_models[model_position].objects.get(connection_id=current_id)
                    url_id = current_id.pk
                    current_id = current_id.pk
                    model_position +=1


            except database_models[model_position].DoesNotExist:
                status = True
        if url_id == None:
            return [ model_position, current_id ]
        return [ model_position, url_id ]

    # Landlord: Data Entry complete status
    def doc_complete(self, bank_id):
        doc_results = self.get_current_model_value(bank_id)
        if doc_results[0] == len(database_models):
            return True
        else:
            return False

    #function returns current property documents url position
    def get_url_namespace(self,bank_id):
        doc_results = self.get_current_model_value(bank_id)
        return [model_urls[doc_results[0]], doc_results[1]]
