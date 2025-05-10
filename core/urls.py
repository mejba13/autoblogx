from django.urls import path
from .views import GeneratePostAPIView

urlpatterns += [
    path('generate-post/', GeneratePostAPIView.as_view(), name='generate-post'),
]
