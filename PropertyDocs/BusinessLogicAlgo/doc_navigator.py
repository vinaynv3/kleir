
from PropertyDocs.models import *
from ImageUpload.models import *

#models
database_models = [Documents,Address,Insights,MarketingValue,Plan,LegalLandmarks,SiteVisitLandmarks,Photos,Maps]
#model relative url namespaces
model_urls = ['doc-loantype','doc-address','doc-insights','doc-market-value','doc-apt-plan',
              'doc-legal-landmarks','doc-site-landmarks','doc-photo','doc-maps','doc-collections']

class Direction:

    #function returns current data entry url position
    def get_url_namespace(self,bank_id):
        doc_results = self.get_current_model_value(bank_id)
        return doc_results[1]

    # function returns current property documents position
    def get_current_model_value(self,bank_id):
        """
        Check BankRef model pk in between models Documents and SiteVisitLandmarks
        """
        current_id = bank_id
        model_position = 0
        status = False
        url_namespace = None

        while model_position < len(database_models) and not status:
            try:
                if database_models[model_position].objects.get(connection_id=current_id):
                    model_position +=1
            except database_models[model_position].DoesNotExist:
                status = True

        if model_position == len(database_models):
            url_namespace = model_urls[model_position]
        else:
            url_namespace = model_urls[model_position]

        return [ model_position, url_namespace ]

    def doc_complete(self, bank_id):
        """
        Document completion status is in relation Data Entry team
        Note: Data entry team doesn't enter technical detail data
        """
        try:
            #Check in final model
            if Maps.objects.get(connection_id=bank_id):
                return True
        except Maps.DoesNotExist:
            return False


class Collection:
    """
    Collects all one-to-one connection_id objects related BankRef model
    starting from model Documents until SiteVisitLandmarks
    """

    def get_model_objects(self,bank_id):

        models = [ database_models[i].objects.get(connection_id = bank_id)
                     for i in range(len(database_models))]
        model_data = { str(type(model).__name__):model.id for model in models }
        return model_data
