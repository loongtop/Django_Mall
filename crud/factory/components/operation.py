from django.utils.safestring import mark_safe
from django.db import models
from django.urls import reverse
from django.http import QueryDict


class Operation(object):
    def __init__(self):
        pass

    @staticmethod
    def checkbox(param, obj: models.Model = None, is_header=None):
        """
        :param param:
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Operation"
        return mark_safe(f'<input type="checkbox" name="pk" value="{obj.pk}" />')

    @staticmethod
    def update(param: dict, obj: models.Model = None, is_header=None):
        """
        :param param:
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Update"

        url = Operation.reverse_url(param, pk=obj.pk)
        return mark_safe(f'<a href="{url}">Update</a>')

    @staticmethod
    def delete(param: dict, obj: models.Model = None, is_header=None):
        """
        :param param:
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Delete"
        url = Operation.reverse_url(param, pk=obj.pk)
        return mark_safe(f'<a href="{url}">Delete</a>')

    @staticmethod
    def reverse_url(param: dict, *args, **kwargs):
        namespace = param.get('namespace')
        url_name = param.get('url_name')
        request = param.get('request')

        fullname = f'{namespace}:{url_name}'
        base_url = reverse(fullname, args=args, kwargs=kwargs)
        if not request.GET:
            add_url = base_url
        else:
            param = request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            url_encode = new_query_dict.urlencode()
            add_url = f"{base_url}?{url_encode}"
        return add_url
