from .factory.factory import CURDFactory
from .factory import products
from .factory.components.operation import Operation
'''
The method of get or create the factory of crud component
All of the objects int the Django are Singleton
'''


def get_create_factory(app_name='', namespace=''):
    return CURDFactory(app_name, namespace)


def get_handler(creat=products.Create, read=products.Read,
                update=products.Update, delete=products.Delete):

    handler_dict = {'create': creat,
                    'read': read,
                    'update': update,
                    'delete': delete}

    return handler_dict
