from django import forms
from shop import models


class HostModelForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(HostModelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
