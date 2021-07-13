from django.urls import path, include
from . import views
urlpatterns = [
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/Viewer', views.ViewDocument, name = 'viewer'),
    ]
