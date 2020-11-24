from django.urls import path, include
from PropertyDocs.views import *

"""

#URL routes - post site vist detail entries
SiteDocs_patterns = [
            path('loan_type/', AddLoanType.as_view(), name='doc-loantype'),
            path('address/', AddAddress.as_view(), name='doc-address'),
            path('property_insights/', PropertyInsights.as_view(), name='doc-insights'),
            ]


#URL routes - Customer entry & Home-Page
"""


urlpatterns = [
    path('', ListCustomers.as_view(), name='Home-Page'),
    path('<slug:slug>/<int:pk>/AddRef/', AddBankRef.as_view(), name='Ref-Num'),
    path('<slug:slug>/<int:pk>/details/', CustomerDetails.as_view(), name='Detail-Page'),
    path('CreateCustomerProfile/', CreateCustomer.as_view(), name='doc-customer'),
    path('<slug:slug>/<int:pk>/update/', UpdateCustomer.as_view(), name='doc-customer-update'),
    path('<slug:slug>/<int:pk>/delete/', DeleteCustomer.as_view(), name='doc-customer-delete')]
    #path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/', include(SiteDocs_patterns)),]
