from abc import ABCMeta, abstractmethod
from django.urls import re_path
from django import forms
from django.urls import reverse


class Handler(metaclass=ABCMeta):
    handler_name = {'read': 'read',
                    'create': 'create',
                    'update': 'update',
                    'delete': 'delete'}

    def __init__(self, model_class, name_dict):
        self._name = self.__class__.__name__.lower()
        self._model_class = model_class
        self._name_dict = name_dict

    @property
    def get_app_model_name(self):
        app_label = self._model_class._meta.app_label
        model_name = self._model_class._meta.model_name

        return f'{app_label}_{model_name}'

    @property
    def get_reverse_name(self):
        return f'{self.get_app_model_name}_{Handler.handler_name[self._name]}'

    @abstractmethod
    def get_url(self):
        pass

    @property
    def get_model_form_class(self):
        class CurrentModelForm(forms.ModelForm):
            class Meta:
                model = self._model_class
                fields = "__all__"

        return CurrentModelForm

    @property
    def reverse_list_url(self):
        name = ''
        base_url = reverse(name)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return f'{base_url}?{param}'










