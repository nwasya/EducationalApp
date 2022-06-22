import itertools
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from Edu_account.forms import CreateCourseForm
from Edu_comment.forms import CommentForm
from Edu_comment.models import CourseComment
from Edu_course.forms import input_form, EditCourseForm, DeleteCourseForm
from Edu_course.models import Course
from Edu_teacher.models import TeacherClass
from Edu_user.models import UserProfile


class CourseListAll(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.all()

class CourseListKids(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(title__icontains='pocket')

class CourseListChildren(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(title__icontains='first')

class CourseListTeenAgers(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(title__icontains='family')


class CourseListAdults(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.search_adults('top','summit')



class CourseListActives(ListView):
    template_name = 'courses/course_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(active=True)






class SearchCoursesView(ListView):
    template_name = 'courses/searched_course_list.html'
    paginate_by = 12

    def get_queryset(self):
        request = self.request

        query = request.GET.get('q')

        if query is not None:

            return  Course.objects.search(query)

        return Course.objects.get_active_courses()







# class ProductsListByCategory(ListView):
#     template_name = 'products/products_list.html'
#     paginate_by = 6
#
#     def get_queryset(self):
#         print(self.kwargs)
#         category_name = self.kwargs['category_name']
#         category = ProductCategory.objects.filter(name__iexact=category_name).first()
#         if category is None:
#             raise Http404('صفحه ی مورد نظر یافت نشد')
#         return Product.objects.get_products_by_category(category_name)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def course_detail(request, *args, **kwargs):
    selected_course_id = kwargs['courseId']

    course = Course.objects.get_by_id(selected_course_id)

    if course is None :
        raise Http404('کلاس مورد نظر یافت نشد')

    if request.method == 'POST':

        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            full_name = comment_form.cleaned_data.get('full_name')
            email = comment_form.cleaned_data.get('email')
            text = comment_form.cleaned_data.get('text')
            course_object = Course.objects.get_by_id(selected_course_id)
            CourseComment.objects.create(full_name=full_name,email=email,text=text,object=course_object).save()

            return HttpResponseRedirect(f'/products/{selected_course_id}/{course_object.title.replace(" ", "-")}')

    comment_list = CourseComment.objects.filter(object__id=selected_course_id,confirmed=True).all()

    form = CommentForm()

    context = {
        'product': course,
        'comments': comment_list,
        'form': form

    }

    return render(request, 'courses/course_detail.html', context)


def course_detail_from_home(request, *args, **kwargs):
    selected_course_id = kwargs['courseId']


    course = Course.objects.get_by_id(selected_course_id)

    if course is None :
        raise Http404('کلاس مورد نظر یافت نشد')

    context = {
        'course': course,


    }

    return render(request, 'home_page.html', context)


li = []

@login_required(login_url='/login')
def edit_course_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    context = {}

    input = input_form()

    if request.method == 'POST':

        if 'جستجو' in request.POST:

            input = input_form(request.POST)

            if input.is_valid():

                course_id_num = input.cleaned_data.get('id_num')

                course_obj = Course.objects.filter(id_num=course_id_num)

                if course_obj.count() > 1:
                    context['choose_course'] = True
                    course_models = Course.objects.filter(id_num=course_id_num)
                    context['course_list'] = course_models

                elif course_obj is None:

                    return Http404
                else:
                    edit_course_form = EditCourseForm(
                        initial={'title': course_obj.title,
                                 'description': course_obj.description,
                                 'price': course_obj.price,
                                 'date': course_obj.starting_date,
                                 'is_active': course_obj.active,

                                 }
                    )
                    id_num = Course.objects.get(id_num=course_id_num).id
                    li.append(id_num)
                    context['edit_form'] = edit_course_form
                    context['confirm'] = True

        if 'ویرایش' in request.POST:
            course = request.POST.get('dropdown')

            course_obj = Course.objects.get(id=int(course))
            li.append(int(course))
            edit_course_form = EditCourseForm(
                initial={'title': course_obj.title,
                         'description': course_obj.description,
                         'price': course_obj.price,
                         'date': course_obj.starting_date,
                         'id_num': course_obj.id_num,
                         'is_active': course_obj.active,
                         }
            )
            context['edit_form'] = edit_course_form
            context['confirm'] = True

        if 'ذخیره' in request.POST:
            print(li)
            course_id_num = Course.objects.get(id=li[-1]).id_num

            course_id = li[-1]

            edit_course_form = EditCourseForm(request.POST)
            course_obj = Course.objects.get(id=course_id)
            print(course_obj)

            if edit_course_form.is_valid():

                title = edit_course_form.cleaned_data.get('title')
                description = edit_course_form.cleaned_data.get('description')
                price = edit_course_form.cleaned_data.get('price')
                date = edit_course_form.cleaned_data.get('date')
                id_num = edit_course_form.cleaned_data.get('id_num')
                is_active = edit_course_form.cleaned_data.get('is_active')

                if id_num is None:
                    id_num = course_id_num

                course_obj.title = title
                course_obj.description = description
                course_obj.price = price
                course_obj.date = date
                course_obj.id_num = id_num
                course_obj.active = is_active
                course_obj.save()
                messages.success(request,"دوره با موفقیت ویرایش شد")


                return redirect('/editcourse')

    context['form'] = input

    return render(request, 'edit_course_page.html', context)


@login_required(login_url='/login')
def create_course_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        course_form = CreateCourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            title = course_form.cleaned_data.get('title')
            description = course_form.cleaned_data.get('description')
            teacher = request.POST['dropdown']

            teacher_obj = TeacherClass.objects.filter(id_num=teacher).first()

            id_num = course_form.cleaned_data.get('id_num')
            date = course_form.cleaned_data.get('date')
            price = course_form.cleaned_data.get('price')

            image = request.FILES['image']
            course_model = Course(title=title, description=description, image=image,
                                  active=True, teacher=teacher_obj, id_num=id_num, starting_date=date, price=price)

            course_model.save()
            messages.success(request,"دوره با موفقیت افزوده شد")
            return HttpResponseRedirect('addcourse')

    course_form = CreateCourseForm()
    teacher_list = TeacherClass.objects.all()

    context = {

        'form': course_form,
        'teacher_list': teacher_list

    }
    return render(request, 'add_course.html', context)



@login_required(login_url='/login')
def delete_course_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    context = {}
    if request.method == 'POST':
        if 'submit' in request.POST:
            course_form = DeleteCourseForm(request.POST)
            if course_form.is_valid():
                id_num = course_form.cleaned_data.get('id_num')

                course_model = Course.objects.filter(id_num=id_num)

                if course_model.count() > 1:
                    context['choose_course'] = True
                    course_models = Course.objects.filter(id_num=id_num)
                    context['course_list'] = course_models
                else:
                    course_model.delete()

        if 'حذف' in request.POST:

            course = request.POST.getlist('dropdown')
            print(course)

            for i in course:
                course_obj = Course.objects.get(id=int(i))
                course_obj.delete()
    course_form = DeleteCourseForm()

    context['form'] = course_form
    return render(request, 'delete_course.html', context)