from django.db import models

# Create your models here.


def file_directory_path(instance, filename):
    return f'static/files/file_{instance.id}_{filename}'


class FileCSV(models.Model):
    file = models.FileField(upload_to=file_directory_path, verbose_name='Ваш файл')


class DataDeal(models.Model):
    customer = models.CharField(max_length=100, verbose_name='Покупатель')
    item = models.CharField(max_length=100, verbose_name='Предмет')
    total = models.IntegerField()
    quantity = models.IntegerField(verbose_name='Количество')
    date = models.DateTimeField()
