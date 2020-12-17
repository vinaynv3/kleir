from django.contrib import admin

from PropertyDocs.models import *
from ImageUpload.models import *

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
