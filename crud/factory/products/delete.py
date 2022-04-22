from .handler import Handler
from django.urls import re_path
from django.shortcuts import render,redirect


class Delete(Handler):
    name = 'delete'

    def get_url(self):
        url = fr'{self.name}/(?P<pk>\d+)/$'
        return re_path(url, super().wrapper(self.delete), name=self.get_reverse_name)

    def delete(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        origin_list_url = self.reverse_url(self.name)
        if request.method == 'GET':
            return render(request, 'crud/delete.html', {'cancel': origin_list_url})

        self.model_class.objects.filter(pk=pk).delete()
        return redirect(origin_list_url)

