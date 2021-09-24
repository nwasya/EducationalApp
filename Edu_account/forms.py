from django import forms
from django.contrib.auth.models import User
from django.core import validators

from Edu_account.models import PassReset
from Edu_book.models import Product
from Edu_course.models import Course



class LoginForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید', 'class': 'fadeIn second'}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید', 'class': 'fadeIn second'}),
        label='کلمه ی عبور'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')

        return user_name


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید'}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا تکرار کلمه عبور خود را وارد نمایید'}),
        label='تکرار کلمه ی عبور'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if len(email) > 20:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 20 باشد')

        else:
            return email

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(password)
        print(re_password)

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password


class CreateBooksForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام کتاب ', 'class': 'form-control'}),
        label='نام کتاب',
        validators=[
            validators.MaxLengthValidator(150, 'نام کتاب')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'توضیحات کتاب ', 'class': 'form-control'}),
        label='توضیحات',

    )
    image = forms.ImageField(label="تصویر کتاب")

    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'قیمت کتاب'}),
                               label='قیمت:', )

    id_num = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': ' کد کتاب ', 'class': 'form-control'}),
        label='کد کتاب',
        validators=[
            validators.MaxValueValidator(999, ' کد کتاب نباید بیشتر از 999 رقم داشته باشد')
        ]
    )

    courseList = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple,
                                                required=False,
                                                label='کلاس مربوطه رو انتخاب کنید (انتخاب بیش از چند کلاس مجاز است،با فشردن دکمه کنترل بر روی صفحه کلید میتوانید بیش از چند کلاس را انتخاب کنید.)',
                                                )

    def clean_id_num(self):
        id_num = self.cleaned_data.get('id_num')
        if Product.objects.filter(id_num=id_num).exists():
            raise forms.ValidationError('کتابی با این کد قبلا ثبت شده است')
        else:
            return id_num


class CreateCourseForm(forms.Form):
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

    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد کلاس را وارد نمایید', 'class': 'form-control'}),
        label='کد کلاس',
        validators=[
            validators.MaxLengthValidator(4, ' کد کلاس نباید بیشتر از 4 رقم داشته باشد')
        ]
    )

    image = forms.ImageField(label="تصویر کلاس")




class DeleteBookForm(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد کتاب را وارد نمایید', 'class': 'form-control'}),
        label='کد کتاب',

    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if Product.objects.filter(id_num=id_num).exists():
            return id_num
        else:
            raise forms.ValidationError('کتاب یافت نشد')


class CreateStudentForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام زبان آموز را وارد نمایید', 'class': 'form-control'}),
        label='نام زبان آموز',
        validators=[
            validators.MaxLengthValidator(150, ' نام زبان آموز نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'لطفا نام خانوادگی زبان آموز را وارد نمایید', 'class': 'form-control'}),
        label='نام خانواگی زبان آموز',
        validators=[
            validators.MaxLengthValidator(150, ' نام خانوادگی نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد ملی زبان آموز را وارد نمایید', 'class': 'form-control'}),
        label='کد ملی',
        validators=[
            validators.MaxLengthValidator(10, ' کد ملی زبان آموز نباید بیشتر از 10 کاراکتر باشد')
        ]
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا شماره زبان آموز را وارد نمایید', 'class': 'form-control'}),
        label='شماره تماس',
        validators=[
            validators.MaxLengthValidator(12, ' شماره زبان آموز نباید بیشتر از 10 کاراکتر باشد')
        ]
    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if User.objects.filter(username=id_num).exists():
            raise forms.ValidationError('blaaaah')
        else:
            return id_num


class DeleteStudentForm(forms.Form):
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


class CreateTeacherForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام دبیر را وارد نمایید', 'class': 'form-control'}),
        label='نام دبیر',
        validators=[
            validators.MaxLengthValidator(150, ' نام دبیر نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خانوادگی دبیر را وارد نمایید', 'class': 'form-control'}),
        label='نام خانوادگی دبیر',
        validators=[
            validators.MaxLengthValidator(150, ' نام خوانوادگی نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد ملی دبیر را وارد نمایید', 'class': 'form-control'}),
        label='کد ملی',
        validators=[
            validators.MaxLengthValidator(10, ' کد ملی دبیر نباید بیشتر از 10 کاراکتر باشد')
        ]
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا شماره تماس دبیر را وارد نمایید', 'class': 'form-control'}),
        label='شماره تماس',
        validators=[
            validators.MaxLengthValidator(12, ' شماره تماس دبیر نباید بیشتر از 10 کاراکتر باشد')
        ]
    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if User.objects.filter(username=id_num).exists():
            raise forms.ValidationError('blaaaah')
        else:
            return id_num


class EditTeacherForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام دبیر را وارد نمایید', 'class': 'form-control'}),
        label='نام دبیر',
        validators=[
            validators.MaxLengthValidator(150, ' نام دبیر نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خانوادگی دبیر را وارد نمایید', 'class': 'form-control'}),
        label='نام خانوادگی دبیر',
        validators=[
            validators.MaxLengthValidator(150, ' نام خوانوادگی نباید بیشتر از 150 کاراکتر باشد')
        ]
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا شماره تماس دبیر را وارد نمایید', 'class': 'form-control'}),
        label='شماره تماس',
        validators=[
            validators.MaxLengthValidator(12, ' شماره تماس دبیر نباید بیشتر از 10 کاراکتر باشد')
        ]
    )


class ChangePassForm(forms.ModelForm):
    class Meta:
        model = PassReset
        fields = '__all__'
        exclude = ()

    password_new = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'لطفا کلمه عبور جدید خود را وارد نمایید', 'class': 'form-control'}),
        label='کلمه عبور جدید'
    )
    re_password_new = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'لطفا تکرار کلمه عبور جدید خود را وارد نمایید', 'class': 'form-control'}),
        label='تکرار کلمه عبور جدید'
    )

    def clean_re_password_new(self):
        new = self.cleaned_data['password_new']
        re_new = self.cleaned_data['re_password_new']
        if new == re_new:
            return re_new
        else:
            raise forms.ValidationError('تکرار رمز صحیح نمی باشد')




class input_2(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'کد  را وارد نمایید', 'class': 'form-control'}),

    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']

        if Product.objects.filter(id_num=id_num).exists():
            return id_num

        else:
            raise forms.ValidationError('کد  در سیستم موجود نمیباشد')


class input_3(forms.Form):
    id_num = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'کد  را وارد نمایید', 'class': 'form-control'}),

    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']

        if Product.objects.filter(id_num=id_num).exists():
            return id_num

        else:
            raise forms.ValidationError('کد  در سیستم موجود نمیباشد')




class EditBookForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کتاب را وارد نمایید', 'class': 'form-control'}),
        label='نام کتاب',
        validators=[
            validators.MaxLengthValidator(150, 'نام کتاب')
        ]
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا  توضیحات کتاب را وارد نمایید', 'class': 'form-control'}),
        label='توضیحات',

    )

    price = forms.IntegerField()

    id_num = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا کد کتاب را وارد نمایید', 'class': 'form-control'}),
        label='کد کتاب',
        validators=[
            validators.MaxValueValidator(999, ' کد کتاب نباید بیشتر از 3 رقم داشته باشد')
        ]
    )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']

        if id_num == '':
            return None
        elif Course.objects.filter(id_num=id_num).exists():
            raise forms.ValidationError('کتابی با این کد قبلا ثبت شده است')
        else:
            return id_num

        class CreateNewsForm(forms.Form):
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
            image = forms.ImageField(label="تصویر خبر")
