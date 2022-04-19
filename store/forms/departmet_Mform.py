from django import forms
from store.models import Department


class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)
        # # Add styles to ModelForm generated fields uniformly
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'