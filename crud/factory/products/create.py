from .handler import Handler
from django.urls import re_path
from django.shortcuts import render, redirect


class Create(Handler):
    name = 'create'

    def create(self, request):
        """
       :param request:
       :return:
       """
        model_form_class = self.get_modelform_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'crud/change.html', {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save_form(form, is_update=False)
            # After the database is successfully saved,
            # jump back to the list page with the original parameters
            return redirect(self.reverse_url(self.handler_name.get('read')))
        return render(request, 'crud/change.html', {'form': form})

    def get_url(self):

        return re_path(fr'{self.name}/$', super().wrapper(self.create), name=self.get_reverse_name)


