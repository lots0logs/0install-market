from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from market.apps.models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App

@parsleyfy
class LoginForm(forms.Form):
    username = forms.CharField(
        label = "Username",
        max_length = 30,
        required = True,
    )

    password = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput,
        max_length = 30,
        required = True,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-signin'
        self.helper.form_class = 'form-signin'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'

        self.helper.add_input(Submit('submit', 'Submit'))
