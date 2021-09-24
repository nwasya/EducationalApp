from django import forms
from django.core import validators
from utilities.BaseFormWithCaptcha import BaseFormWithCaptcha

class CreateRegisterForm(BaseFormWithCaptcha):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام و نام خانوادگی خود را وارد نمایید','class':'form-control'}),
        label='نام و نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(150, 'نام و نام خانوادگی نباید بیش از 150 کاراکتر باشد')
        ]
    )

    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد ملی خود را وارد نمایید','class':'form-control'}),
        label='کدملی',
        validators=[
            validators.MaxLengthValidator(15, 'کدملی نباید بیشتر از 15 کاراکتر باشد')
        ]

    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا شماره تماس خود را وارد نمایید', 'class': 'form-control'}),
        label='شماره تماس',
        validators=[
            validators.MaxLengthValidator(20, 'شماره تماس نباید بیشتر از 20 کاراکتر باشد')
        ]

    )

    latest_course = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'اگر قبلا در دوره ای شرکت نکرده اید،متن را خالی بگذارید','class':'form-control'}),
        label='آخرین دوره',
        validators=[
            validators.MaxLengthValidator(200, 'نام آخرین دوره نباید بیش از 200 کاراکتر باشد')
        ]
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'لطفا آدرس محل زندگی خود را وارد نمیید',
            'class': 'form-control'}),
        label='آدرس',
        validators=[
            validators.MaxLengthValidator(300, 'آدرس نباید بیش از 300 کاراکتر باشد')
        ]
    )

    birth = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا سال تولد خود را وارد نمایید', 'class': 'form-control'}),
        label='سال تولد',

        validators=[
            validators.MaxLengthValidator(4, 'سال تولد باید معتبر باشد')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا وضعیت تحصیلی و سطح یادگیری و زبان خود را شرح دهید','class':'form-control','rows':'8'}),
        label='متن توضیحات',

    )
