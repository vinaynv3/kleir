from django.urls import path, include
from . import views
urlpatterns = [
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/layoutEntry/', views.LayoutView, name = 'technical-layout'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/BUAEntry/', views.BUA_View, name = 'technical-BUA'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/PropertyValue/', views.PropertyValueView, name = 'technical-PropertyValue'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/FairMarket/', views.FinalNotesView, name = 'technical-FairMarket'),
    ]
