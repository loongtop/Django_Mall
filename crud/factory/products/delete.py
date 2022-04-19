from .handler import Handler
from django.urls import re_path
from django.shortcuts import render


class Delete(Handler):

    def get_url(self):
        url = r'delete/(?P<pk>\d+)/$'
        return re_path(url, self.delete, name=self.get_reverse_name)

    def delete(self, request):
        return ''

