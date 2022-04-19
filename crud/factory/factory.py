from django.urls import re_path
from abc import ABCMeta, abstractmethod


class Factory(metaclass=ABCMeta):

    @abstractmethod
    def register(self, model_class, handler_dict):
        pass

    @abstractmethod
    def get_urls(self):
        pass

    @abstractmethod
    def urls(self):
        pass


class CURDFactory(Factory):
    """
    Singleton
    """
    def __init__(self, app_name, namespace):
        if not hasattr(CURDFactory, "_first_init"):
            self._registry = []
            self.app_name = app_name
            self.namespace = namespace

    def register(self, *args, **kwargs):
            for model in args:
                for item in model:
                    self._registry.append({'model_class': item[0], 'handler_dict': item[1]})

    def create_urls(self, model_class, handler_dict):
        patterns = []
        name_dict = {'app_name': self.app_name,
                     'namespace': self.namespace}

        for key, value in handler_dict.items():
            operator = value(model_class, name_dict)
            url = operator.get_url()
            patterns.append(url)

        return patterns

    def get_urls(self):
        """
        get_url
        :return:
        """
        patterns = []
        for model in self._registry:
            obj = model['model_class']
            handler_dict = model['handler_dict']
            app_label = obj._meta.app_label
            model_name = obj._meta.model_name

            patterns.append(re_path(fr'^{app_label}/{model_name}/', (self.create_urls(obj, handler_dict), None, None)))

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

