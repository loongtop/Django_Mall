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

    def register(self, *args, prev=None):
        for model in args:
            for item in model:
                self._registry.append({'model_class': item[0], 'handler_dict': item[1], 'prev': prev})

    def create_urls(self, model_class, handler_dict, prev):
        patterns = []
        name_dict = {'app_name': self.app_name,
                     'namespace': self.namespace}

        for _, operator_item in handler_dict.items():
            operator = operator_item(model_class, name_dict, prev)
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
            prev = model['prev']
            app_label = obj._meta.app_label
            model_name = obj._meta.model_name

            if prev:
                patterns.append(
                    re_path(fr'^{app_label}/{model_name}/{prev}', (self.create_urls(obj, handler_dict, prev), None, None)))
            else:
                patterns.append(
                    re_path(fr'^{app_label}/{model_name}/', (self.create_urls(obj, handler_dict, prev), None, None)))

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

