from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # def ready(self):
    #     autodiscover_modules('store_curd')
