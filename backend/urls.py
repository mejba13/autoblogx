import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views  # ✅ Fix added here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', core_views.custom_login, name='login'),
    path('auth/register/', core_views.custom_register, name='register'),
    path('api/', include('core.urls')),  # If you're using API endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
