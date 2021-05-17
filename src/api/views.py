import threading
import traceback

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FileCSV
from api.serializers import FileCSVSerializer, InfoTopClientSerializer
from api.services import create_data_deal, get_data


@api_view(['GET'])
def main_api_view(request):
    """Method for checking api"""
    return Response({'status': 'ok'})


class FileCSVList(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or posted.
    """
    queryset = FileCSV.objects.all()
    serializer_class = FileCSVSerializer

    # Переопределние сохранения файла
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Сохранение данных в бд по id файла

            thread1 = threading.Thread(
                target=create_data_deal(serializer.data['id']),
            )
            thread1.start()
            return Response({'status': 'OK - файл был обработан без ошибок'})
        except Exception:
            return Response(
                {'status': f'Error, Desc: {traceback.format_exc()} - в процессе обработки файла произошла ошибка.'})


class InfoTopClientView(APIView):

    def get(self, request):
        return Response(get_data())
