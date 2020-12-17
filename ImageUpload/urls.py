from django.urls import path, include
from . import views


urlpatterns = [
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/Photos/', views.PhotoView, name = 'doc-photo'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/Maps/', views.MapsView, name = 'doc-maps'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/Photos/<int:photo_id>', views.PhotoUpdate, name = 'doc-photo-update'),
    path('<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/Maps/<int:map_id>', views.MapsUpdate, name = 'doc-map-update'),
    ]
