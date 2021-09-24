

from django import forms
from django.contrib.auth.models import User
from django.core import validators

from Edu_account.models import PassReset
from Edu_book.models import Product
from Edu_course.models import Course
from Edu_user.models import Student

from utilities.BaseFormWithCaptcha import BaseFormWithCaptcha


class input_form(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'کد  را وارد نمایید', 'class': 'form-control'}),

    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']

        if Course.objects.filter(id_num=id_num).exists():
            return id_num

        else:
            raise forms.ValidationError('کد  در سیستم موجود نمیباشد')
class EditCourseForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کلاس را وارد نمایید', 'class': 'form-control'}),
        label='نام کلاس',
        validators=[
            validators.MaxLengthValidator(150, ' نام کلاس نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا  توضیحات کلاس را وارد نمایید', 'class': 'form-control'}),
        label='توضیحات',

    )

    price = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا هزینه ترم را وارد نمایید', 'class': 'form-control'}),
        label='هزینه ترم',

    )

    date = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا تاریخ شروع را وارد نمایید', 'class': 'form-control'}),
        label='تاریخ شروع'
    )

    id_num = forms.CharField(required=False,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'لطفا کد کلاس را وارد نمایید', 'class': 'form-control'}),
                             label='کد کلاس',
                             validators=[
                                 validators.MaxLengthValidator(4, ' کد کلاس نباید بیشتر از 4 رقم داشته باشد')
                             ]
                             )
    NUMS = [
        ('False', 'غیر فعال است'),
        ('True', 'فعال است'),

    ]
    is_active = forms.CharField(widget=forms.RadioSelect(choices=NUMS), label='آیا کلاس در حال حاضر فعال است  ')

class DeleteCourseForm(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد کلاس را وارد نمایید', 'class': 'form-control'}),
        label='کد کلاس',
        validators=[
            validators.MaxLengthValidator(4, ' کد کلاس نباید بیشتر از 4 رقم داشته باشد')
        ]
    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if Course.objects.filter(id_num=id_num).exists():
            return id_num
        else:
            raise forms.ValidationError('کلاس یافت نشد')
