from .handler import Handler
from django.urls import re_path
from django.shortcuts import render, redirect
from django.http import HttpResponse


class Update(Handler):
    name = 'update'

    def get_url(self):
        url = fr'{self.name}/(?P<pk>\d+)/$'
        return re_path(url, super().wrapper(self.update), name=self.get_reverse_name)

    # dui硬change_view
    def update(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        current_change_object = self.model_class.objects.filter(pk=pk).first()
        if not current_change_object:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        model_form_class = self.get_modelform_class()
        if request.method == 'GET':
            form = model_form_class(instance=current_change_object)
            return render(request, 'crud/change.html', {'form': form})
        form = model_form_class(data=request.POST, instance=current_change_object)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_url(self.name))
        return render(request, 'crud/change.html', {'form': form})
