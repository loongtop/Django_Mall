from .factory.factory import CURDFactory


def get_create_factory(app_name='', namespace=''):
    return CURDFactory(app_name, namespace)