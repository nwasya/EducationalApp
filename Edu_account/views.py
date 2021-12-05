from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView

from Edu_Mark.models import Mark
from Edu_Sregister.models import RegisteredStudent

from Edu_book.models import Product
from Edu_comment.forms import CommentForm
from Edu_comment.models import ProductComment, CourseComment
from Edu_contact.models import ContactUs
from Edu_course.models import Course

from Edu_order.models import OrderDetail, Order

from Edu_register.models import Register
from Edu_teacher.models import TeacherClass
from Edu_user.models import UserProfile, Student
from .forms import LoginForm, CreateBooksForm, CreateStudentForm, CreateTeacherForm, \
    ChangePassForm, DeleteStudentForm, DeleteBookForm, \
    EditTeacherForm,  EditBookForm, input_2


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':

        if login_form.is_valid():

            user_name = login_form.cleaned_data.get('user_name')

            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                first_name = request.user.first_name
                last_name = request.user.last_name

                messages.info(request, f" {first_name} {last_name} عزیز ، به وبسایت آموزشی استقلال خوش آمدید .")
                return redirect('/')
            else:
                login_form.add_error('password', 'رمز نا معتبر است.')

    context = {

        'login_form': login_form

    }
    return render(request, 'account/login_page.html', context)


def log_out(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def user_account(request):
    return render(request, 'user_account.html', {})


@login_required(login_url='/login')
def create_books_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        books_form = CreateBooksForm(request.POST, request.FILES)
        if books_form.is_valid():
            title = books_form.cleaned_data.get('title')
            description = books_form.cleaned_data.get('description')
            price = books_form.cleaned_data.get('price')
            image = request.FILES['image']
            course = request.POST.getlist('dropdown')

            print(course)
            if str(course) == "NONE":
                course_obj = None
                li = None
            else:
                li = []

            id_num = books_form.cleaned_data.get('id_num')
            book_model = Product(title=title, description=description, image=image, active=True, price=price,
                                 id_num=id_num)

            book_model.save()
            messages.success(request, 'کتاب جدید با موفقیت ثبت شد')
            for i in course:
                if li is None:
                    break
                elif book_model.course.filter(id=i).exists():
                    pass
                else:
                    book_model.course.add(i)

            return HttpResponseRedirect('/addbook')
        else:
            messages.error(request,
                           mark_safe('متاسفانه هنگام ثبت،خطایی رخ داد.لطفا موارد زیر را در نظر داشته باشید: <br/>'
                                     'موضوع کتاب نباید بیش از 150 کاراکتر باشد <br/>'
                                     'اضافه کردن تصویر اجباری می باشد   <br/>'
                                     'شناسه کتاب باید بین 1 و 999 باشد.'))

    books_form = CreateBooksForm()
    course = Course.objects.all()
    context = {

        'form': books_form,
        'course_list': course,

    }
    return render(request, 'add_books.html', context)


@login_required(login_url='/login')
def delete_book_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        course_form = DeleteBookForm(request.POST, request.FILES)
        if course_form.is_valid():
            id_num = course_form.cleaned_data.get('id_num')
            title = Product.objects.get(id_num__exact=id_num).title
            product = Product.objects.filter(id_num__exact=id_num).delete()
            messages.success(request, f'کتاب {title} با موفقیت حذف شد.')

            return HttpResponseRedirect('deletebook')

    book_form = DeleteBookForm()

    context = {

        'form': book_form,

    }
    return render(request, 'delete_book.html', context)





@login_required(login_url='/login')
def create_student_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':

        student_form = CreateStudentForm(request.POST, request.FILES)
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            id_num = student_form.cleaned_data.get('id_num')
            phone_number = student_form.cleaned_data.get('phone_number')
            course = request.POST['course']
            role = 'Student'
            course_obj = Course.objects.get(id=course)
            try:
                Student.objects.create(first_name=first_name, last_name=last_name, id_num=id_num, course=course_obj
                                       , role=role,
                                       phone_number=phone_number)

                user = User.objects.create_user(username=id_num, password=id_num, first_name=first_name,
                                                last_name=last_name)
                UserProfile.objects.create(user=user, role=role, full_name=first_name + ' ' + last_name)
                messages.success(request, 'زبان آموز جدید با موفقیت ثبت شد')
            except:
                messages.error(request,'خطایی در ثبت رخ داد')


            return HttpResponseRedirect('/addstudent')

    student_form = CreateStudentForm()
    course_list = Course.objects.filter(active=True)

    context = {

        'form': student_form,
        'course_list': course_list

    }
    return render(request, 'add_student.html', context)


@login_required(login_url='/login')
def delete_student_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':

        student_form = DeleteStudentForm(request.POST, request.FILES)
        if student_form.is_valid():
            id_num = student_form.cleaned_data.get('id_num')

            student = Student.objects.filter(id_num=id_num)
            print(student)
            user = User.objects.filter(username=id_num).delete()

            return HttpResponseRedirect('/deletestudent')

    student_form = DeleteStudentForm()

    context = {

        'form': student_form,

    }
    return render(request, 'delete_student.html', context)


@login_required(login_url='/login')
def create_teacher_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':

        teacher_form = CreateTeacherForm(request.POST, request.FILES)
        if teacher_form.is_valid():
            first_name = teacher_form.cleaned_data.get('first_name')
            last_name = teacher_form.cleaned_data.get('last_name')
            id_num = teacher_form.cleaned_data.get('id_num')
            phone_number = teacher_form.cleaned_data.get('phone_number')
            role = 'Teacher'
            TeacherClass.objects.create(first_name=first_name, last_name=last_name, id_num=id_num, role=role,
                                        phone_number=phone_number)

            user = User.objects.create_user(username=id_num, password=id_num, first_name=first_name,
                                            last_name=last_name)
            UserProfile.objects.create(user=user, role=role, full_name=first_name + ' ' + last_name)

            return HttpResponseRedirect('/addteacher')

    teacher_form = CreateTeacherForm()

    context = {

        'form': teacher_form,

    }
    return render(request, 'add_teacher.html', context)


@login_required(login_url='/login')
def delete_teacher_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        teacher = request.POST['dropdown']

        x = TeacherClass.objects.filter(id_num=teacher).first()

        first_name = x.first_name
        last_name = x.last_name

        TeacherClass.objects.filter(id_num=teacher).delete()
        UserProfile.objects.filter(full_name=first_name + ' ' + last_name).delete()

    teacher_list = TeacherClass.objects.all()
    context = {
        'teacher_list': teacher_list
    }
    return render(request, 'delete_teacher.html', context)


class ShowContactsInfo(ListView):
    template_name = 'show_contact.html'
    paginate_by = 2

    def get_queryset(self):
        return ContactUs.objects.all()

    def get_redirect_url(self, *args, **kwargs):
        user_role = UserProfile.objects.get(user=self.request.user_name).role
        if user_role == 'Manager':

            pass
        else:
            print('ok')
            return reverse('/')


class ShowRegistrationRequests(ListView):
    template_name = 'show_register.html'
    paginate_by = 2

    def get_queryset(self):
        return Register.objects.all()


@login_required(login_url='/login')
def change_password(request):
    form = ChangePassForm(request.POST, request.user)
    pass
    #
    # if request.method == 'POST':
    #
    #     if form.is_valid():
    #         user2 = form.save(commit=False)
    #
    #         password_new = form.cleaned_data.get("newpassword1")
    #         re_password_new = form.cleaned_data.get("newpassword2")
    #         if password_new == re_password_new:
    #             user = User.objects.get(username=request.user.username)
    #             user.set_password(re_password_new)
    #             user.save()
    #
    #             messages.add_message(request, messages.INFO, 'رمز با موفقیت تغییر یافت')
    #
    #         else:
    #             messages.add_message(request, messages.ERROR, 'در وارد کردن اطلاعات دقت کنید')
    #     else:
    #         form = ChangePassForm()
    # return render(request, 'change_password.html', {
    #
    #     'form': form
    #
    # })


li = []



@login_required(login_url='/login')
def unconfirmedcomments(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    product_comments = CourseComment.objects.filter(confirmed=False)
    course_comments = ProductComment.objects.filter(confirmed=False)

    context = {

        'product_comments': product_comments,
        'course_comments': course_comments,

    }

    return render(request, 'show_unconfirmed_comments.html', context)


@login_required(login_url='/login')
def confirmedcomments(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    product_comments = CourseComment.objects.filter(confirmed=True)
    course_comments = ProductComment.objects.filter(confirmed=True)

    form = CommentForm()

    context = {

        'product_comments': product_comments,
        'course_comments': course_comments,
        'form': form,

    }
    return render(request, 'show_confirmed_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, *args, **kwargs):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    comment_id = kwargs.get('comment_id')

    if comment_id is not None:
        if CourseComment.objects.get_by_id(comment_id) is not None:
            CourseComment.objects.get_by_id(comment_id).delete()
            return redirect('/showcomments')
        elif ProductComment.objects.get_by_id(comment_id) is not None:
            ProductComment.objects.get_by_id(comment_id).delete()
            return redirect('/showcomments')
        else:
            raise Http404

    product_comments = CourseComment.objects.filter(confirmed=True)
    course_comments = ProductComment.objects.filter(confirmed=True)

    form = CommentForm()

    context = {

        'product_comments': product_comments,
        'course_comments': course_comments,
        'form': form,

    }
    return render(request, 'show_confirmed_comments.html', context)


@login_required(login_url='/login')
def confirm_comment(request, *args, **kwargs):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    comment_id = kwargs.get('comment_id')

    if comment_id is not None:

        if CourseComment.objects.get_by_id(comment_id) is not None:

            x = CourseComment.objects.get(id=comment_id).confirmed

            CourseComment.objects.set_status_comment(comment_id)

            if x:

                return redirect('/showcomments')
            else:
                return redirect('/unconfirmedcomments')

        elif ProductComment.objects.get_by_id(comment_id) is not None:
            x = ProductComment.objects.get(id=comment_id).confirmed
            ProductComment.objects.set_status_comment(comment_id)
            if x:

                return redirect('/showcomments')
            else:
                return redirect('/unconfirmedcomments')
        else:
            raise Http404




li = []


@login_required(login_url='/login')
def edit_teacher_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    global teacher_id_num
    global edit_teacher_form

    context = {}
    context['confirm'] = False

    if request.method == 'POST':

        if 'جستجو' in request.POST:

            teacher_id_num = request.POST.get('dropdown')

            li.append(teacher_id_num)
            context['teacher_id_num'] = teacher_id_num
            teacher_obj = TeacherClass.objects.get(id_num=teacher_id_num)
            edit_teacher_form = EditTeacherForm(
                initial={'first_name': teacher_obj.first_name,
                         'last_name': teacher_obj.last_name,
                         'phone_number': teacher_obj.phone_number}
            )

            if teacher_obj is None:
                return Http404
            else:
                context['edit_form'] = edit_teacher_form
                context['confirm'] = True

        if 'ذخیره' in request.POST:

            teacher_id_num = li[-1]
            edit_teacher_form = EditTeacherForm(request.POST)
            teacher_obj = TeacherClass.objects.get(id_num=teacher_id_num)

            if edit_teacher_form.is_valid():
                first_name = edit_teacher_form.cleaned_data.get('first_name')
                last_name = edit_teacher_form.cleaned_data.get('last_name')
                phone_number = edit_teacher_form.cleaned_data.get('phone_number')

                teacher_obj.first_name = first_name
                teacher_obj.last_name = last_name
                teacher_obj.phone_number = phone_number
                teacher_obj.save()
                return redirect('/editteacher')

    teacher_list = TeacherClass.objects.all()

    context['teacher_list'] = teacher_list

    return render(request, 'edit_teacher_page.html', context)


@login_required(login_url='/login')
def edit_book_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    context = {}

    input = input_form()

    if request.method == 'POST':

        if 'جستجو' in request.POST:

            input = input_2(request.POST)

            if input.is_valid():

                book_id_num = input.cleaned_data.get('id_num')

                li.append(book_id_num)
                print(book_id_num)

                book_obj = Product.objects.get(id_num=book_id_num)
                print(book_obj)
                edit_book_form = EditBookForm(
                    initial={'title': book_obj.title,
                             'description': book_obj.description,
                             'price': book_obj.price,
                             'id_num': book_obj.id_num,

                             }
                )

                if book_obj is None:
                    messages.error(request, 'کتاب با شناه وارد شده،یافت نشد')
                else:
                    context['edit_form'] = edit_book_form
                    context['confirm'] = True

        if 'ذخیره' in request.POST:

            book_id_num = li[-1]

            edit_book_form = EditBookForm(request.POST)
            book_obj = Product.objects.get(id_num=book_id_num)

            if edit_book_form.is_valid():

                title = edit_book_form.cleaned_data.get('title')
                description = edit_book_form.cleaned_data.get('description')
                price = edit_book_form.cleaned_data.get('price')

                id_num = edit_book_form.cleaned_data.get('id_num')
                if id_num is None:
                    id_num = book_id_num

                book_obj.title = title
                book_obj.description = description
                book_obj.price = price
                book_obj.id_num = id_num
                book_obj.save()
                messages.success(request, 'تغییرات با موفقیت اعمال گردید')
                return redirect('/editbook')
            else:
                messages.error(request,
                               mark_safe('متاسفانه هنگام ثبت،خطایی رخ داد.لطفا موارد زیر را در نظر داشته باشید: <br/>'
                                         'موضوع کتاب نباید بیش از 150 کاراکتر باشد <br/>'
                                         'اضافه کردن تصویر اجباری می باشد   <br/>'
                                         'شناسه کتاب باید بین 1 و 999 باشد.'))

    context['form'] = input

    return render(request, 'edit_book_page.html', context)


#
# @login_required(login_url='/login')
# def edit_student_page(request):
#     context = {}
#
#     input = input_3()
#
#     if request.method == 'POST':
#
#         if 'جستجو' in request.POST:
#
#             input = input_3(request.POST)
#
#             if input.is_valid():
#
#                 student_id_num = input.cleaned_data.get('id_num')
#                 li.append(student_id_num)
#                 print(student_id_num)
#
#                 student_obj = Student.objects.get(id_num=student_id_num)
#                 print(student_obj)
#                 edit_student_form = EditStudentForm(
#                     initial={'title': student_obj.title,
#                              'description': student_obj.description,
#                              'price': student_obj.price,
#                              'id_num': student_obj.id_num,
#
#                              }
#                 )
#
#                 if student_obj is None:
#                     return Http404
#                 else:
#                     context['edit_form'] = edit_student_form
#                     context['confirm'] = True
#
#         if 'ذخیره' in request.POST:
#
#             book_id_num = li[-1]
#
#             edit_student_form = EditBookForm(request.POST)
#             student_obj = Product.objects.get(id_num=book_id_num)
#
#             if edit_student_form.is_valid():
#
#                 title = edit_student_form.cleaned_data.get('title')
#                 description = edit_student_form.cleaned_data.get('description')
#                 price = edit_student_form.cleaned_data.get('price')
#
#                 id_num = edit_student_form.cleaned_data.get('id_num')
#                 if id_num is None:
#                     id_num = student_id_num
#
#                 student_obj.title = title
#                 student_obj.description = description
#                 student_obj.price = price
#                 student_obj.id_num = id_num
#                 student_obj.save()
#                 return redirect('/')
#
#     context['form'] = input
#
#     return render(request, 'edit_book_page.html', context)

@login_required(login_url='/')
def recent_orders(request):
    obj = OrderDetail.objects.all().order_by('-order__payment_date')
    li = []
    dic = {}

    for item in obj:

        if item.product.id_num in li:
            temp = []
            temp = dic[item.product.id_num]
            temp[0] += item.count
            dic[item.product.id_num] = temp

        else:
            temp = []
            li.append(item.product.id_num)
            title = Product.objects.get(id_num=item.product.id_num).title
            payment_date = item.order.payment_date


            temp.append(item.count)
            temp.append(title)
            temp.append(payment_date)


            dic[item.product.id_num] = temp

    context = {

        'dic': dic,

    }
    return render(request, 'recent_orders.html', context)


@login_required(login_url='/')
def order_detail(request):
    li = []
    main_dic = {}
    inner_dic = {}

    orders = Order.objects.filter(is_paid=True).order_by('-payment_date')
    counter = 0

    for item in orders:

        id_num = item.owner.username
        order_details = OrderDetail.objects.filter(order__owner__username=id_num).reverse()

        for detail in order_details:

            if detail.product.id_num in li:
                temp = []
                temp = inner_dic[detail.product.id_num]
                temp[0] += detail.count
                inner_dic[detail.product.id_num] = temp


            else:
                temp = []
                li.append(detail.product.id_num)
                title = Product.objects.get(id_num=detail.product.id_num).title

                temp.append(detail.count)
                temp.append(title)


                inner_dic[detail.product.id_num] = temp

        temp = []
        li = []

        name = f'{item.owner.first_name} {item.owner.last_name}'

        serial_num = item.seril_num
        temp.append(name)
        temp.append(inner_dic)
        inner_dic = {}
        temp.append(serial_num)
        temp.append(item.payment_date)
        main_dic[counter] = temp
        counter += 1
        print(main_dic)

    context = {

        'dic': main_dic,

    }
    return render(request, 'order_detail.html', context)


@login_required(login_url='/')
def recent_registration(request):
    dic = {}
    counter = 0

    obj = RegisteredStudent.objects.all().order_by('-time')


    for item in obj:
        if item.course is None:
            return Http404

        dic[counter] = [f'{item.student.first_name} {item.student.last_name}', item.course, item.time, item.course.price]
        counter += 1

    context = {

        'dic': dic

    }
    return render(request, 'recent_registration.html', context)


@login_required(login_url='/')
def add_online_class_link(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Teacher':
        return redirect('/')
    if request.method == 'POST':
        class_link = request.POST['class-link']
        course = request.POST['course']

        course_obj = Course.objects.get(id_num=course)
        if course_obj is None:
            raise Http404
        else:
            course_obj.online_class_link = str(class_link)
            course_obj.save()

    user_id = request.user.username
    teacher = TeacherClass.objects.filter(id_num=user_id).first()
    course = Course.objects.filter(teacher=teacher)

    context = {'course': course,

               }

    return render(request, 'add-online-class-link.html', context)




@login_required(login_url='/login')
def transfer_student(request):
    global course_name,id_num,id_nums,des_course_id
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    context = {}
    context['course_flag'] = True
    context['des_course_flag'] = False
    context['student_flag'] = False
    context['course_items'] = Course.objects.all().order_by('id_num')

    if request.method == 'POST':

        if 'course' in request.POST:

            course_id = request.POST['course']

            course_id = Course.objects.get(id=course_id).id
            student = Student.objects.filter(course__id=course_id )

            context['student'] = student
            context['student_flag'] = True
            context['course_flag'] = False
            context['des_course_flag'] = False


        if 'students' in request.POST:
            id_nums = request.POST.getlist('students')
            print(id_nums)

            context['student_flag'] = False
            context['des_course_flag'] = True
            context['course_flag'] = False



        if 'des_course' in request.POST:
            des_course_id = request.POST['des_course']

            des_course_obj = Course.objects.get(id=des_course_id)
            for student in id_nums:
                x = Student.objects.get(id_num=student)
                x.course = des_course_obj
                x.save()



            messages.success(request, "کلاس دانش آموزان با موفیقیت انتقال یافت")
            return redirect('/transfer-student')

    return render(request, 'transfer_student.html', context)
