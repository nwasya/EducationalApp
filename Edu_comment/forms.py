from django import forms
from django.contrib.auth.models import User
from django.core import validators
from utilities.BaseFormWithCaptcha import BaseFormWithCaptcha


class CommentForm(BaseFormWithCaptcha):


    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی', 'class': 'form-control'}),

        validators=[
            validators.MaxLengthValidator(150, 'نام نباید بیش از 150 کاراکتر باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید','class':'form-control'}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا  متن پیام را وارد نمایید', 'class': 'form-control'}),


    )
