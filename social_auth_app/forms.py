from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext as _


class DetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = u'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = u'Last Name'

        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Div('country', css_class='country-selector'),
        #     HTML('<h2>Tell us more about yourself...</h2>'),
        #     PrependedText('first_name', 'Name'),
        #     PrependedText('last_name', 'Surname'),
        #     ButtonHolder(
        #         Submit('next', 'Next', css_class='btn-primary')
        #     )
        # )

    class Meta:
        model = get_user_model()
        fields = ( 'first_name', 'last_name',)
        # widgets = {'country': CountrySelectWidget()}


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = u'Email address'
        self.fields['password'].widget.attrs['placeholder'] = u'Password'

        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Div(
        #         'username', css_class='input-wrapper'
        #     ),
        #     Div(
        #         'password', css_class='input-wrapper'
        #     ),
        #     ButtonHolder(
        #         Submit('login', 'Login', css_class='btn-primary')
        #     )
        # )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                return self.cleaned_data
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data