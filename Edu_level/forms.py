
from django import forms
from django.contrib.auth.models import User
from django.core import validators


class CreateLevelForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام سطح را وارد نمایید', 'class': 'form-control'}),
        label='نام سطح',
        validators=[
            validators.MaxLengthValidator(150, ' نام سطح نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '، این بخش از توضیحات در صفحه ای مجزا نمایش داده خواهد شد .لطفا  توضیحات کامل را وارد نمایید', 'class': 'form-control'}),
        label='توضیحات تکمیلی',

    )

    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'این بخش از توضیحات در صفحه اصلی نمایش داده خواهد شد،ترجیحا هر توضیح را در سطر مجزا جهت معرفی دوره بنویسید', 'class': 'form-control'}),
        label='توضیح کوتاه',

    )


    image = forms.ImageField(label="تصویر ")



class EditLevelForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام سطح را وارد نمایید', 'class': 'form-control'}),
        label='نام سطح',
        validators=[
            validators.MaxLengthValidator(150, ' نام سطح نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '، این بخش از توضیحات در صفحه ای مجزا نمایش داده خواهد شد .لطفا  توضیحات کامل را وارد نمایید', 'class': 'form-control'}),
        label='توضیحات تکمیلی',

    )

    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'این بخش از توضیحات در صفحه اصلی نمایش داده خواهد شد،ترجیحا هر توضیح را در سطر مجزا جهت معرفی دوره بنویسید', 'class': 'form-control'}),
        label='توضیح کوتاه',

    )
