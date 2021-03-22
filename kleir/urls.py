
"""
kleir URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('PropertyDocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('ImageUpload.urls')),
    path('', include('Technical.urls')),
    path('', include('Reports.urls')),
    path('', include('Viewer.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
