from rest_framework import serializers

from api.models import FileCSV


class FileCSVSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileCSV
        fields = ('id', 'file')
        read_only_fields = ('id',)


class InfoTopClientSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    spent_money = serializers.IntegerField()
    gems = serializers.JSONField()
