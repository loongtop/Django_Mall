from .handler import Handler
from django.urls import re_path
from django.shortcuts import render, redirect


class Create(Handler):

    def create(self, request):
        """
               添加页面
               :param request:
               :return:
               """
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'stark/change.html', {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def get_url(self):
        url = r'create/'
        return re_path(url, super().wrapper(self.create), name=self.get_reverse_name)


