from django import forms
from django.contrib.auth.models import User
from django.core import validators


class DeleteMarkForm(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد ملی زبان آموز را وارد نمایید', 'class': 'form-control'}),
        label='کد ملی',
        validators=[
            validators.MaxLengthValidator(10, ' کد ملی زبان آموز نباید بیشتر از 10 کاراکتر باشد')
        ]
    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if User.objects.filter(username=id_num).exists():
            return id_num
        else:
            raise forms.ValidationError('این کد ملی در سیستم موجود نیست')


class CreateMarkForm(forms.Form):
    class_activity = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '50', 'step': '0.01', 'class': 'form-control-lg'}),
        label='فعالیت کلاسی')

    quizzes = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '50', 'step': '0.01', 'class': 'form-control-lg'}),
        label='کوییز ها'
    )
    midterm = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '50', 'step': '0.01', 'class': 'form-control-lg'}),
        label='میانترم',
        # validators=[
        #     validators.MaxValueValidator(20, 'نمره میانترم نباید بزرگتر از 35 باشد')
        # ]
    )

    final = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '60', 'step': '0.01', 'class': 'form-control-lg'}),
        label='فاینال',
        # validators=[
        #     validators.MaxValueValidator(20, 'نمره فاینال نباید بزرگتر از 40 باشد')
        # ]
    )

    extra_mark = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '30', 'step': '0.01', 'class': 'form-control-lg'}),
        label='نمره اضافی',
        # validators=[
        #     validators.MaxValueValidator(20, 'نمره اضافی نباید بزرگتر از 10 باشد')
        # ]

    )

    total_mark = forms.FloatField(widget=forms.TextInput(
        attrs={'type': 'number', 'min': '0', 'max': '101', 'step': '0.01', 'class': 'form-control-lg'}),
        label='نمره نهایی',

    )

    description = forms.CharField(label='توضیحات',
        widget=forms.Textarea(attrs={'placeholder': 'لطفا توضیحات مربوط را وارد کنید', 'class': 'form-control'}),

    )
