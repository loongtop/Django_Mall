from django.urls import re_path
from crud import get_create_factory
from shop.models import UserInfo, Department, Deploy
from shop.views import userinfo, department, deploy
from crud import get_handler


register_item = ((UserInfo, userinfo.handler_dict),
                 (Deploy, deploy.handler_dict),
                 (Department, department.handler_dict),)


def get_shop_urls(namespace, app_name='CRUD', item=register_item):
    factory = get_create_factory(app_name, namespace)

    factory.register(item)

    return [re_path('', factory.urls)]
