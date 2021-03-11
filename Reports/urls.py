from django.urls import path, include
from . import views
urlpatterns = [
    path('Reports/', views.ReportsHomeView, name = 'multi-filter-search'),
    path('Reports/display/', views.ReportsDispalyView, name = 'multi-filter-search-display'),
    ]
