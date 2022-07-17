from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from django_filters import FilterSet, NumberFilter
from django.utils.translation import gettext, gettext_lazy as _

from .models import DiseasedUser, SpecialDoctor, StatusDiseasedUser

User = get_user_model()


class CreateDiseasedForm(ModelForm):
    class Meta:
        model = DiseasedUser
        exclude = ['type_of_doctors', 'is_doctor_view']


class UpdateDiseasedForm(ModelForm):
    class Meta:
        model = DiseasedUser
        fields = ['type_of_doctors']


class StatusDiseasedUserForm(ModelForm):
    class Meta:
        model = StatusDiseasedUser
        exclude = ['diseased', 'doctor']


class CreateDoctorForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SpecialDoctor
        exclude = ['is_admin', 'is_active', 'is_doctor', 'last_login']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_tel_number(self):
        tel_number = self.cleaned_data.get('tel_number')
        qs = User.objects.filter(tel_number=tel_number)
        if qs.exists():
            raise forms.ValidationError("tel_number is taken")
        return tel_number


class FilterForm(FilterSet):
    number = NumberFilter(
        field_name='pk', label='Enter number of registration',
        widget=forms.NumberInput(attrs={'placeholder': 'type something ...'}))

    class Mete:
        model = DiseasedUser


#
# class RegisterForm(ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
#
#     class Meta:
#         model = User
#         fields = ['email', 'tel_number', 'first_name', 'last_name']
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("email is taken")
#         return email
#
#     def clean_tel_number(self):
#         tel_number = self.cleaned_data.get('tel_number')
#         qs = User.objects.filter(tel_number=tel_number)
#         if qs.exists():
#             raise forms.ValidationError("tel_number is taken")
#         return tel_number
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password2")
#         if password is not None and password != password2:
#             self.add_error("password2", "Your passwords must match")
#         return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'tel_number', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password is not None and password != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['tel_number', 'first_name', 'last_name', 'email', 'password', 'is_active']

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    tel_number = forms.CharField(max_length=55)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
