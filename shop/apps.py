from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    # def ready(self):
    #     autodiscover_modules('shop_curd')
