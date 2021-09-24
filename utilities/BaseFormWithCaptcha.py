from django import forms
from captcha.fields import ReCaptchaV3, ReCaptchaField


class BaseFormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(
        label='تصویر امنیتی',
        widget=ReCaptchaV3(api_params={
            'hl': 'fa'
        }),
        error_messages={
            'required': 'لطفا تصویر امنیتی را تایید کنید'
        }
    )
