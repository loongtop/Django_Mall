from django.urls import re_path
from crud import get_create_factory
from shop.models import UserInfo, Host, Department
from shop.views import department, userinfo, host


register_item = ((UserInfo, userinfo.handler_dict),
                 (Host, host.handler_dict),
                 (Department, department.handler_dict),)


def get_shop_urls(namespace, app_name='CRUD', item=register_item):
    factory = get_create_factory(app_name, namespace)

    factory.register(item)

    urlpatterns = [re_path('', factory.urls)]

    return urlpatterns
