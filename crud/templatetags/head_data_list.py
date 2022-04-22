from django import template
from types import FunctionType

register = template.Library()


def get_head(data_pack):
    display_list = data_pack.display

    if display_list:
        for key_or_func in display_list:
            if isinstance(key_or_func, FunctionType):
                param = {}
                verbose_name = key_or_func(param, obj=None, is_header=True)
            else:
                verbose_name = data_pack.model_class._meta.get_field(key_or_func).verbose_name
            yield verbose_name
    else:
        yield data_pack.model_class._meta.model_name


def get_data(data_pack):
    for row in data_pack.data_list:
        if not data_pack.display:
            yield row
            continue

        tr_list = []
        for key_or_func in data_pack.display:
            if isinstance(key_or_func, FunctionType):
                name = key_or_func.__name__
                url_name = data_pack.get_app_model_name(name)
                param = {'request': data_pack.request,
                         'namespace': data_pack.name_dict['namespace'],
                         'url_name': url_name}
                val = key_or_func(param, row, is_header=False)
            else:
                val = getattr(row, key_or_func)

            tr_list.append(val)
        yield tr_list


@register.inclusion_tag('crud/head_data_list.html')
def head_data_list(data_pack):

    return {'head_list': get_head(data_pack), 'data_list': get_data(data_pack)}

