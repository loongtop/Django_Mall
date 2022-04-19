import functools
from types import FunctionType
from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.http import QueryDict
from django import forms
from django.db.models import Q
from django.db.models import ForeignKey, ManyToManyField
from stark.utils.pagination import Pagination
from django.db.models import ForeignKey, ManyToManyField


def get_choice_text(title, field):
    """
    When defining a column in the component,
    if the choice wants to display Chinese information, just call this method.
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """
    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = f"get_{field}_display"
        return getattr(obj, method)()

    return inner
