from django.urls import path, include
from . import views
urlpatterns = [
    path('Reports/', views.ReportsHomeView, name = 'multi-filter-search'),
    path('Reports/display/<int:page>/', views.ReportsDispalyView, name = 'multi-filter-search-display'),
    path('Reports/display/<slug:slug>/<int:pk>/<str:bank_type>/<int:bank_id>/', views.ReportOptions, name = 'single-report-options'),
    ]
