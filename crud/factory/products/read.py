from .handler import Handler
from django.urls import re_path
from django.shortcuts import render
from types import FunctionType
from crud.utils.pagination import Pagination

from django.db.models import Q
from .bootstrap import BootstrapModelForm

from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import QueryDict
from django.db import models


class Read(Handler):
    display_list = []

    def __init__(self, model_class, name_dict, prev):
        super().__init__(model_class, name_dict, prev)

        self.per_page_count = 2
        self.has_create_btn = True
        self.pager = None
        self.request = None


    @property
    def display(self):
        value = []
        value.extend(self.display_list)
        return value

    def get_head_body_list(self, data_list):
        # 处理显示表头
        head_list = []
        display_list = self.display

        if display_list:
            for key_or_func in display_list:
                if isinstance(key_or_func, FunctionType):
                    verbose_name = key_or_func(self, obj=None, is_header=True)
                else:
                    verbose_name = self._model_class._meta.get_field(key_or_func).verbose_name
                head_list.append(verbose_name)
        else:
            head_list.append(self._model_class._meta.model_name)

        # 处理表的内容
        body_list = []
        for row in data_list:
            tr_list = []
            if display_list:
                for key_or_func in display_list:
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, is_header=False))
                    else:
                        tr_list.append(getattr(row, key_or_func))  # obj.gender
            else:
                tr_list.append(row)
            body_list.append(tr_list)

        return head_list, body_list

    def read(self, request):
        """
        :param request:
        :return:
        """

        objects = self._model_class.objects.all()
        cnt = objects.count()
        params = request.GET.copy()
        params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=cnt,
            base_url=request.path_info,
            query_params=params,
            per_page=self.per_page_count,

        )

        data_list = objects[pager.start: pager.end]
        head_list, body_list = self.get_head_body_list(data_list)

        return render(request, 'crud/changelist.html', {'data_list': data_list,
                                                        'head_list': head_list,
                                                        'body_list': body_list,
                                                        'pager': pager})

    def changelist_view(self, request, *args, **kwargs):
        """
        列表页面
        :param request:
        :return:
        """
        # ########## 1. 处理Action ##########
        action_list = self.get_action_list()
        action_dict = {func.__name__: func.text for func in action_list}  # {'multi_delete':'批量删除','multi_init':'批量初始化'}

        if request.method == 'POST':
            action_func_name = request.POST.get('action')
            if action_func_name and action_func_name in action_dict:
                action_response = getattr(self, action_func_name)(request, *args, **kwargs)
                if action_response:
                    return action_response

        # ########## 2. 获取排序 ##########
        search_list = self.get_search_list()
        search_value = request.GET.get('q', '')
        conn = Q()
        conn.connector = 'OR'
        if search_value:
            for item in search_list:
                conn.children.append((item, search_value))

        # ########## 3. 获取排序 ##########
        order_list = self.get_order_list()
        # 获取组合的条件
        search_group_condition = self.get_search_group_condition(request)
        queryset = self.model_class.objects.filter(conn).filter(**search_group_condition).order_by(*order_list)

        # ########## 4. 处理分页 ##########
        all_count = queryset.count()

        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        data_list = queryset[pager.start:pager.end]

        # ########## 5. 处理表格 ##########
        list_display = self.get_list_display()
        # 5.1 处理表格的表头
        header_list = []
        if list_display:
            for key_or_func in list_display:
                if isinstance(key_or_func, FunctionType):
                    verbose_name = key_or_func(self, obj=None, is_header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(key_or_func).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)

        # 5.2 处理表的内容

        body_list = []
        for row in data_list:
            tr_list = []
            if list_display:
                for key_or_func in list_display:
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, is_header=False))
                    else:
                        tr_list.append(getattr(row, key_or_func))  # obj.gender
            else:
                tr_list.append(row)
            body_list.append(tr_list)

        # ########## 6. 添加按钮 #########
        add_btn = self.get_add_btn()

        # ########## 7. 组合搜索 #########
        search_group_row_list = []
        search_group = self.get_search_group()  # ['gender', 'depart']
        for option_object in search_group:
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_group_row_list.append(row)

        return render(
            request,
            'crud/changelist.html',
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn,
                'search_list': search_list,
                'search_value': search_value,
                'action_dict': action_dict,
                'search_group_row_list': search_group_row_list
            }
        )

    def get_create_btn(self):
        if self.has_create_btn:
            namespace = self._name_dict.get('namespace')

            name = Handler.handler_name.get('create')
            reverse_name = f'{namespace}:{self.get_app_model_name}_{name}'
            create_url = reverse(reverse_name)
            return f'<a class="btn btn-primary" href="{create_url}">Create</a>'
        return None

    def get_model_form_class(self):
        if self._model_class:
            return self._model_class

        class DynamicModelForm(BootstrapModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    def get_order_list(self):
        return self.order_list or ['-id', ]

    def get_search_list(self):
        return self.search_list

    def get_action_list(self):
        return self.action_list

    def get_search_group(self):
        return self.search_group

    def get_search_group_condition(self, request):
        """
        获取组合搜索的条件
        :param request:
        :return:
        """
        condition = {}
        # ?depart=1&gender=2&page=123&q=999
        for option in self.get_search_group():
            if option.is_multi:
                values_list = request.GET.getlist(option.field)  # tags=[1,2]
                if not values_list:
                    continue
                condition['%s__in' % option.field] = values_list
            else:
                value = request.GET.get(option.field)  # tags=[1,2]
                if not value:
                    continue
                condition[option.field] = value
        return condition

    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除（如果想要定制执行成功后的返回值，那么就为action函数设置返回值即可。）
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    def get_url(self):

        return re_path(r'read/$', super().wrapper(self.read), name=self.get_reverse_name)

    def checkbox(self, obj: models.Model = None, is_header=None):
        """
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Operation"
        return mark_safe(f'<input type="checkbox" name="pk" value="{obj.pk}" />')

    def update(self, obj: models.Model = None, is_header=None):
        """
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Update"

        url = self.reverse_url(pk=obj.pk, name='update')
        return mark_safe(f'<a href="{url}">Update</a>')

    def delete(self, obj: models.Model = None, is_header=None):
        """
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "Delete"
        url = self.reverse_url(pk=obj.pk, name='delete')
        return mark_safe(f'<a href="{url}">Delete</a>')

    def reverse_url(self, name, *args, **kwargs):

        namespace = self._name_dict['namespace']
        url_name = self.get_app_model_name(name)
        fullname = f'{namespace}:{url_name}'
        base_url = reverse(fullname, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "{base_url}?{new_query_dict.urlencode()}"
        return add_url



