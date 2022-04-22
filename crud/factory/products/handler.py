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
        self.model_class = model_class
        self.name_dict = name_dict
        self.prev = prev
        self.request = None
        self._modelform = None
        self.request = None
        self.model_form_class = None

    def get_app_model_name(self, param):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name

        if self.prev:
            return f'{app_label}_{model_name}_{self.prev}_{param}'
        return f'{app_label}_{model_name}_{param}'

    @property
    def get_reverse_name(self):
        return f'{self.get_app_model_name(Handler.handler_name[self._name])}'

    @abstractmethod
    def get_url(self):
        pass

    # customize the you own ModelForm which contain clean_name function etc.
    def get_modelform_class(self):

        if model_form_class := self.model_form_class:
            return model_form_class

        class DynamicModelForm(BootstrapModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    def save_form(self, form, is_update=False):
        """
        Hook method reserved before saving data with ModelForm
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

    def reverse_url(self, name,  *args, **kwargs):
        """
        When jumping back to the list page, generate the URL
        :return:
        """
        reverse_name = f"{self.name_dict.get('namespace')}:{self.get_app_model_name(name)}"
        # update del create
        if name == 'update':
            base_url = reverse(reverse_name)
        base_url = reverse(reverse_name, args=args, kwargs=kwargs)

        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = f'{base_url}?{param}'

        return add_url

    def reverse_read_url(self):
        """
        When jumping back to the list page, generate the URL
        :return:
        """
        reverse_name = f"{self.name_dict.get('namespace')}:{self.get_app_model_name('read')}"
        base_url = reverse(reverse_name)
        param = self.request.GET.get('_filter')

        if not param:
            return base_url
        return f'{base_url}?{param}'













