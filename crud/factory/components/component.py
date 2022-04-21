
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import QueryDict


class Component(object):

    def __init__(self, request, namespace, model_class):
        self.request = request
        self.namespace = namespace
        self.model_class = model_class

    def checkbox(self, obj=None, is_header=None):
        """
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' % obj.pk)

    def edit(self, obj=None, is_header=None):
        """
        自定义页面显示的列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "编辑"
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_change_url(pk=obj.pk))

    def delete(self, obj=None, is_header=None):
        if is_header:
            return "删除"
        return None
        # return mark_safe('<a href="%s">删除</a>' % self.reverse_delete_url(pk=obj.pk))

    def reverse_change_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的编辑URL
        :param args:
        :param kwargs:
        :return:
        """
        name = "%s:%s" % (self.namespace, self.get_url_name('change'),)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param,)
        return '%s_%s_%s' % (app_label, model_name, param,)









