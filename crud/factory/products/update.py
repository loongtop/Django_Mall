from .handler import Handler
from django.urls import re_path
from django.shortcuts import render


class Update(Handler):
    def get_url(self):
        url = r'update/(?P<pk>\d+)/$'
        return re_path(url, self.update, name=self.get_reverse_name)

    def update(self, request):
        return ''
