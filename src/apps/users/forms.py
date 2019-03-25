from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from apps.users.models import User


class UserLoginForm(forms.Form):
    """
    Login user.
    """
    username = forms.CharField(label=_('帳號'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('密碼'))
    # This field just for identity validate inactive error in views.py
    is_active = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('您輸入的帳號或密碼不正確，請重試'))
            if not user.is_active:
                self.cleaned_data['is_active'] = False
                raise forms.ValidationError(_('請先啟用您的帳戶'))

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    Includes all the required fields, plus a repeated password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    help_text = """Raw passwords are not stored, so there is no way to see this user's password,
                   but you can change the password using <a href="../password/">this form</a>."""
    password = ReadOnlyPasswordHashField(label='Password', help_text=help_text)

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
