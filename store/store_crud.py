from django.urls import re_path

from crud import get_create_factory
from store.models import Client, Department
from store.views import client, department


register_item = ((Client, client.handler_dict),
                 (Department, department.handler_dict,))


def get_store_urls(namespace, app_name='CRUD', item=register_item):

    factory = get_create_factory(app_name, namespace)

    factory.register(item)

    return [re_path('', factory.urls)]
