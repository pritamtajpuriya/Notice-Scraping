
from asyncio import streams
from urllib import response
from urllib.request import urlopen
from django.db import models

# Create your models here.


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     title = models.CharField(max_length=100, unique=True, primary_key=True)

#     def __str__(self):
#         return self.title

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from requests import request
import requests


class Notice(models.Model):

    title = models.CharField(max_length=250, blank=True)
    date = models.DateField()
    file = models.FileField(upload_to='static/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    belongs = models.CharField(max_length=100)
    file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    # def get_image_from_url(self, url):

    #     response = requests.get(url, streams=True)

    #     file_tmp = NamedTemporaryFile(delete=True)

    #     file_tmp.flush()
    #     file = File(file_tmp)
    #     self.file.save(file_tmp.name, file)
    #     self.file_url = url
