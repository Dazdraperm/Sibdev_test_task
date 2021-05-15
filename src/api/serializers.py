from rest_framework import serializers

from api.models import FileCSV


class FileCSVSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileCSV
        fields = ('id', 'file')
        read_only_fields = ('id',)
