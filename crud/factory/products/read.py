from django.urls import re_path, reverse
from django.shortcuts import render
from types import FunctionType
from django.db.models import Q

from .handler import Handler
from crud.utils.pagination import Pagination


class Read(Handler):
    name = 'read'
    display_list = []

    def __init__(self, model_class, name_dict, prev):
        super().__init__(model_class, name_dict, prev)

        self.per_page_count = 3
        self.pager = None
        self.request = None
        self.component = None
        self.name_dict = name_dict

    @property
    def display(self):
        value = []
        value.extend(self.display_list)
        return value

    def read(self, request):
        """
        :param request:
        :return:
        """

        objects = self.model_class.objects.all()
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

        data_pack = DataPack(self, data_list, pager,)

        return render(request, 'crud/changelist.html', {'data_pack': data_pack})

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

        return re_path(fr'{self.name}/$', super().wrapper(self.read), name=self.get_reverse_name)

########################
    has_create_btn = True

    def get_create_btn(self):
        if self.has_create_btn:
            namespace = self.name_dict.get('namespace')

            name = Handler.handler_name.get('create')
            reverse_name = f'{namespace}:{self.get_app_model_name}_{name}'
            create_url = reverse(reverse_name)
            return f'<a class="btn btn-primary" href="{create_url}">Create</a>'
        return None


class DataPack(object):
    def __init__(self, config, data_list, pager):
        self.config = config
        self.data_list = data_list
        self.display = config.display
        self.model_class = config.model_class
        self.pager = pager
        self.get_app_model_name = config.get_app_model_name
        self.request = config.request
        self.name_dict = config.name_dict





