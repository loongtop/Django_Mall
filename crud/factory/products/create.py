from .handler import Handler
from django.urls import re_path
from django.shortcuts import render,redirect
from django import forms


class Create(Handler):

    def create(self, request):
        """
        :param request:
        :return:
        """
        model_form = self.get_model_form_class
        if request.method == 'GET':
            form = model_form()
            return render(request, 'crud/create.html', {'form': form})

        form = model_form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.reverse_list_url())
        return render(request, 'crud/change.html', {'form': form})

    def get_url(self):
        url = r'create/'
        return re_path(url, self.create, name=self.get_reverse_name)


