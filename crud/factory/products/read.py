from .handler import Handler
from django.urls import re_path
from django.shortcuts import render
from django.utils.safestring import mark_safe
from types import FunctionType
from crud.utils.pagination import Pagination
from django.urls import reverse


class Read(Handler):

    per_page_count = 2
    has_create_btn = True
    _display_list = []

    @property
    def display(self):
        return self._display_list

    def get_create_btn(self):
        if self.has_create_btn:
            namespace = self._name_dict.get('namespace')

            name = Handler.handler_name.get('create')
            reverse_name = f'{namespace}:{self.get_app_model_name}_{name}'
            create_url = reverse(reverse_name)
            return f'<a class="btn btn-primary" href="{create_url}">Create</a>'
        return None

    def get_url(self):

        return re_path(r'read/$', self.read, name=self.get_reverse_name)

    def read(self, request):
        """
        :param request:
        :return:
        """

        objects = self._model_class.objects.all()
        count = objects.count()
        params = request.GET.copy()
        params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=count,
            base_url=request.path_info,
            query_params=params,
            per_page=self.per_page_count,

        )

        data_list = objects[pager.start:pager.end]

        head_list = []

        for name in self.display:
            title = self._model_class._meta.get_field(name).verbose_name
            head_list.append(title)

        body_list = []
        for row in data_list:
            tr_list = []
            for name in self.display:
                tr_list.append(getattr(row, name))
            body_list.append(tr_list)

        btn = self.get_create_btn()
        return render(request, 'crud/change.html', {'data_list': data_list,
                                                    'head_list': head_list,
                                                    'body_list': body_list,
                                                    'pager': pager,
                                                    'btn': btn})

    def partial_display(self, request):
        """
        :param request:
        :return:
        """

        head_list = []
        for name_or_func in self.display:
            if isinstance(name_or_func, FunctionType):
                title = name_or_func(self, obj=None, is_head=True)
            else:
                title = self._model_class._meta.get_field(name_or_func).verbose_name
            head_list.append(title)

        data_list = self._model_class.objects.all()

        body_list = []
        for row in data_list:
            tr_list = []
            for name_or_func in self.display:
                if isinstance(name_or_func, FunctionType):
                    title = name_or_func(self, row, is_head=False)
                else:
                    tr_list.append(getattr(row, name_or_func))
            body_list.append(tr_list)

        return render(request, 'crud/change.html', {'head_list': head_list, 'body_list': body_list})

    def display_update(self, obj=None, is_header=None):
        if is_header:
            return 'Update'
        return mark_safe(r'<a href="https://www.google.com/">Update</a>')

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return 'Delete'
        return mark_safe(r'<a href="https://www.google.com/">Delete</a>')
