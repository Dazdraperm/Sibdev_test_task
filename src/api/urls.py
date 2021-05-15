from django.urls import path
from rest_framework import routers

from api.views import main_api_view, FileCSVList

router = routers.SimpleRouter()
router.register(r'FileCSV', FileCSVList)

urlpatterns = [
    path('', main_api_view, name='main'),
    # path('FileCSV/', FileCSVList, name='FileCSV')
    *router.urls,
]
