from django.urls import path, include
from PropertyDocs.views import *
from PropertyDocs.business_logic_views import *

#URL routes - post site vist detail entries
SiteDocs_patterns = [
            path('navigator/', DirectionView.re_direct, name='doc-navigator'),
            path('loan_type/', AddLoanType.as_view(), name='doc-loantype'),
            path('address/', AddAddress.as_view(), name='doc-address'),
            path('insights/', AddInsights.as_view(), name='doc-insights'),
            path('MarketingValue/', AddMarketingValue.as_view(), name='doc-market-value'),
            path('AptPlan/', AddAptPlan.as_view(), name='doc-apt-plan'),
            path('LegalLandmarks/', AddLegalLandmarks.as_view(), name='doc-legal-landmarks'),
            path('SiteVisitLandmarks/', AddSiteVisitLandmarks.as_view(), name='doc-site-landmarks'),
            ]

SiteDocs_update_patterns = [
            path('collections/', Collections.as_view(), name='doc-collections'),]

Bank_Ref_url_patterns = [
            path('AddBankRefNum/', AddBankRef.as_view(), name='Ref-Num'),
            path('<str:bank_type>/<int:bank_id>/UpdateBankRefNum/', UpdateBankRef.as_view(), name='Ref-Num-update'),
            path('<str:bank_type>/<int:bank_id>/DeleteBankRefNum/', DeleteBankRef.as_view(), name='Ref-Num-delete'),
            ]


urlpatterns = [
    path('', ListCustomers.as_view(), name='Home-Page'),
    path('<slug:slug>/<int:pk>/details/', CustomerDetails.as_view(), name='Detail-Page'),
    path('CreateCustomerProfile/', CreateCustomer.as_view(), name='doc-customer'),
    path('<slug:slug>/<int:pk>/update/', UpdateCustomer.as_view(), name='doc-customer-update'),
    path('<slug:slug>/<int:pk>/delete/', DeleteCustomer.as_view(), name='doc-customer-delete'),
    path('<slug:slug>/<int:pk>/', include(Bank_Ref_url_patterns)),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/', include(SiteDocs_patterns)),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/', include(SiteDocs_update_patterns)),]
