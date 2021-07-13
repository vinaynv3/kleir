from django.urls import path, include
from . import views
from .views import TechnicalCollections
urlpatterns = [
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/position/', views.Position, name = 'technical-navigation'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/layoutEntry/', views.LayoutView, name = 'technical-layout'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/BUAEntry/', views.BUA_View, name = 'technical-BUA'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/PropertyValue/', views.PropertyValueView, name = 'technical-PropertyValue'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/FairMarket/', views.FinalNotesView, name = 'technical-FairMarket'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/technical_docs/', TechnicalCollections.as_view(), name = 'update-templates'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/layoutEntry_update/', views.LayoutViewUpdate, name = 'technical-layout-update'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/BUAEntry_update/', views.BUA_View_Update, name = 'technical-BUA-update'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/PropertyValue_update/', views.PropertyValueViewUpdate, name = 'technical-PropertyValue-update'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/FairMarket_update/', views.FinalNotesViewUpdate, name = 'technical-FairMarket-update'),
    ]
