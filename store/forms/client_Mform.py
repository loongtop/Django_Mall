from django import forms
from store.models import Client


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'first_name', 'second_name',
                  'password', 'confirmed_password', 'phone',
                  'email', 'age', 'gender', 'company']

    def __init__(self, *args, **kwargs):
        super(ClientModelForm, self).__init__(*args, **kwargs)
        # Add styles to ModelForm generated fields uniformly
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
