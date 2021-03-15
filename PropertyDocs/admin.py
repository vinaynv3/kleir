from django.contrib import admin

from PropertyDocs.models import *
from ImageUpload.models import *
from Technical.models import *

# Register your models here.
#PropertyDocs
admin.site.register(ClientInfo)
admin.site.register(BankRef)
admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(Insights)
admin.site.register(MarketingValue)
admin.site.register(Plan)
admin.site.register(LegalLandmarks)
admin.site.register(SiteVisitLandmarks)

#ImageUpload
admin.site.register(Photos)
admin.site.register(Images)
admin.site.register(Maps)
admin.site.register(ImageMaps)

#Technical
admin.site.register(AsPerDocuments)
admin.site.register(AsPerPlan)
admin.site.register(Actuals)
admin.site.register(Deviations)
admin.site.register(PermissibleBUA)
admin.site.register(ActualBUA)
admin.site.register(SanctionedArea)
admin.site.register(AreaDetails)
admin.site.register(Rate)
admin.site.register(TotalValue)
admin.site.register(FairMarketValue)
admin.site.register(PropertyStatus)
admin.site.register(FinalNotes)
