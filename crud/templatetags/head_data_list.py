from django import template
from types import FunctionType

register = template.Library()


def get_head(data_pack):
    head_list = []
    display_list = data_pack.display

    if display_list:
        for key_or_func in display_list:
            if isinstance(key_or_func, FunctionType):
                param = {}
                verbose_name = key_or_func(param, obj=None, is_header=True)
            else:
                verbose_name = data_pack.model_class._meta.get_field(key_or_func).verbose_name
            head_list.append(verbose_name)
    else:
        head_list.append(data_pack._model_class._meta.model_name)
    return head_list


def get_data(data_pack):
    body_list = []
    display_list = data_pack.display
    for row in data_pack.data_list:
        tr_list = []
        if display_list:
            for key_or_func in display_list:
                if isinstance(key_or_func, FunctionType):
                    name = key_or_func.__name__
                    url_name = data_pack.get_app_model_name(name)
                    param = {'request': data_pack.request, 'namespace': data_pack.name_dict['namespace'], 'url_name': url_name}
                    tr_list.append(key_or_func(param, row, is_header=False))
                else:
                    tr_list.append(getattr(row, key_or_func))  # obj.gender
        else:
            tr_list.append(row)
        body_list.append(tr_list)

    return body_list


@register.inclusion_tag('crud/head_data_list.html')
def head_data_list(data_pack):

    head_list = get_head(data_pack)
    data_list = get_data(data_pack)

    return {'head_list': head_list, 'data_list': data_list}

