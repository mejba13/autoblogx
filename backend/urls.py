import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)