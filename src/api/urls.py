from django.urls import path

from api.views import main_api_view

urlpatterns = [
    path('', main_api_view, name='main'),
]
