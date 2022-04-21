from abc import ABCMeta, abstractmethod
from django.urls import re_path
from django import forms
from django.urls import reverse
from .bootstrap import BootstrapModelForm
import functools
from django.http import QueryDict


class Handler(metaclass=ABCMeta):

    handler_name = {'read': 'read',
                    'create': 'create',
                    'update': 'update',
                    'delete': 'delete'}

    def __init__(self, model_class, name_dict, prev):
        self._name = self.__class__.__name__.lower()
        self._model_class = model_class
        self._name_dict = name_dict
        self.prev = prev
        self.request = None

    def get_app_model_name(self, param):
        app_label = self._model_class._meta.app_label
        model_name = self._model_class._meta.model_name

        if self.prev:
            return f'{app_label}_{model_name}_{self.prev}_{param}'
        return f'{app_label}_{model_name}_{param}'

    @property
    def get_reverse_name(self):
        return f'{self.get_app_model_name(Handler.handler_name[self._name])}'

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

    def save_form(self, form, is_update=False):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param form:
        :param is_update:
        :return:
        """
        form.save()

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def extra_urls(self):
        return []












