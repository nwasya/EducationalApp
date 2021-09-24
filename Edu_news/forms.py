from django import forms
from django.contrib.auth.models import User
from django.core import validators

class CreateNewsForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا موضوع خبر را وارد نمایید', 'class': 'form-control'}),
        label='موضوع',
        validators=[
            validators.MaxLengthValidator(150, 'موضوع نباید بیش از 150 کاراکتر باشد')
        ]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'متن خبر را وارد نمایید', 'class': 'form-control'}),
        label=' متن خبر',

    )
    image = forms.ImageField(label="تصویر خبر",required=False)


class EditNewsForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا موضوع خبر را وارد نمایید', 'class': 'form-control'}),
        label='موضوع',
        validators=[
            validators.MaxLengthValidator(150, 'موضوع نباید بیش از 150 کاراکتر باشد')
        ]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا  خبر را وارد نمایید', 'class': 'form-control'}),
        label='خبر',

    )
