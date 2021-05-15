from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def main_api_view(request):
    """Method for checking api"""
    return Response({'status': 'ok'})
