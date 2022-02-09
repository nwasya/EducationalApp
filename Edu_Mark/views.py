from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from Edu_Mark.forms import CreateMarkForm, DeleteMarkForm
from Edu_Mark.models import Mark

from Edu_course.models import Course
from Edu_teacher.models import TeacherClass
from Edu_user.models import UserProfile, Student


# test git

@login_required(login_url='/login')
def enter_mark_page(request):
    global course_name, student_name
    if UserProfile.objects.get(user__username=request.user.username).role != 'Teacher':
        return redirect('/')
    context = {
        'course_flag': True,
        'student_flag': False,
        'mark_flag': False,

    }
    mark_form = CreateMarkForm()
    if request.method == 'POST':

        print(request.POST)

        if 'course' in request.POST:
            print("entexab")
            course_id = request.POST['course']
            course_name = Course.objects.get(id=course_id)
            student = Student.objects.filter(course__id=course_id)

            context['student'] = student
            context['student_flag'] = True
            context['course_flag'] = False

        if 'student' in request.POST:
            print("vared")
            context['student_flag'] = False
            context['course_flag'] = False
            context['mark_flag'] = True
            id_num = request.POST['student']

            mark_form = CreateMarkForm()
            student_name = Student.objects.get(id_num=id_num)

            context['full_name'] = f"{student_name.first_name} {student_name.last_name}"
            context['class_name'] = course_name.title
            x = Mark.objects.filter(student_name=student_name, course_name=course_name).exists()
            if x:
                student = Student.objects.filter(course=course_name)
                context['student'] = student
                messages.info(request,
                              "برای این دانش آموز قبلا نمره ای ثبت شده است. می توانید از پنل ویرایش نمره آن را ویرایش کنید")
                context['student_flag'] = True
                context['course_flag'] = False
                context['mark_flag'] = False
                user_id = request.user.username

                teacher = TeacherClass.objects.filter(id_num=user_id).first()

                course = Course.objects.filter(teacher=teacher, active=True)
                context['course'] = course

                context['form'] = mark_form
                return render(request, 'enter_mark.html', context)

        if 'send' in request.POST:
            mark_form = CreateMarkForm(request.POST)

            if mark_form.is_valid():

                class_activity = mark_form.cleaned_data['class_activity']
                midterm = mark_form.cleaned_data['midterm']
                final = mark_form.cleaned_data['final']
                quizzes = mark_form.cleaned_data['quizzes']
                extra_mark = mark_form.cleaned_data['extra_mark']
                total_mark = mark_form.cleaned_data['total_mark']
                total_work = request.POST['total_work']
                description = mark_form.cleaned_data['description']
                writing = request.POST['writing']
                homework = request.POST['homework']
                listening = request.POST['listening']
                speaking = request.POST['speaking']
                activity = request.POST['activity']

                x = Mark.objects.create(student_name=student_name, course_name=course_name,
                                        class_activity=class_activity,
                                        quizzes=quizzes, midterm=midterm, final=final,
                                        extra_mark=extra_mark, total_mark=total_mark,
                                        total_work=total_work,
                                        description=description, activity=activity,
                                        speaking=speaking, listening=listening,
                                        writing=writing, homework=homework,
                                        )
                x.save()
                student_name.is_registered = False
                student_name.save()

                messages.info(request, "نمره با موفقیت وارد شد")
                return HttpResponseRedirect('/add-mark')
            else:
                messages.error(request, 'خطا در ثبت نمره')

    user_id = request.user.username

    teacher = TeacherClass.objects.filter(id_num=user_id).first()

    course = Course.objects.filter(teacher=teacher, active=True)
    context['course'] = course

    context['form'] = mark_form
    return render(request, 'enter_mark.html', context)


@login_required(login_url='/login')
def view_student_report(request):
    global course_name, student_name
    if UserProfile.objects.get(user__username=request.user.username).role != 'Teacher':
        return redirect('/')
    context = {
        'course_flag': True,
        'student_flag': False,
        'mark_flag': False,

    }
    mark_form = CreateMarkForm()
    if request.method == 'POST':

        if 'course' in request.POST:
            print("entexab")
            course_id = request.POST['course']
            course_name = Course.objects.get(id=course_id)
            student = Student.objects.filter(course__id=course_id, )

            context['student'] = student
            context['student_flag'] = True
            context['course_flag'] = False

        if 'student' in request.POST:
            print("vared")
            context['student_flag'] = False
            context['course_flag'] = False
            context['mark_flag'] = True
            id_num = request.POST['student']
            course_name = Student.objects.filter(id_num=id_num).first().course
            context['teacher'] = course_name.teacher
            marks = Mark.objects.filter(student_name__id_num=id_num, course_name=course_name).first()
            student_name = Student.objects.get(id_num=id_num)
            if marks is not None:
                context['activity'] = get_mark_value(marks.activity)
                context['speaking'] = get_mark_value(marks.speaking)
                context['listening'] = get_mark_value(marks.listening)
                context['writing'] = get_mark_value(marks.writing)
                context['homework'] = get_mark_value(marks.homework)

                context['total_work'] = get_mark_value(marks.total_work)

                mean = context['activity'] + context['speaking'] + context['listening'] + context['writing'] + context[
                    'homework'] + context['total_work']
                context['mean'] = mean / 6

                context['marks'] = marks
                full_Name = f'{student_name.first_name} {student_name.last_name}'
            else:
                context['marks'] = None
                full_Name = f'{student_name.first_name} {student_name.last_name}'

            context['full_name'] = full_Name

    user_id = request.user.username

    teacher = TeacherClass.objects.filter(id_num=user_id).first()

    course = Course.objects.filter(teacher=teacher, active=True)
    context['course'] = course

    context['form'] = mark_form
    return render(request, 'view_student_report.html', context)


@login_required(login_url='/login')
def edit_mark_page(request):
    global course_name, id_num
    if UserProfile.objects.get(user__username=request.user.username).role != 'Teacher':
        return redirect('/')
    context = {}
    context['course_flag'] = True

    if request.method == 'POST':

        if 'course' in request.POST:
            print("entexab")
            course_id = request.POST['course']

            course_name = Course.objects.get(id=course_id)
            student = Student.objects.filter(course__id=course_id)

            context['student'] = student
            context['student_flag'] = True
            context['course_flag'] = False

        if 'student' in request.POST:
            id_num = request.POST['student']

            marks = Mark.objects.filter(student_name__id_num=id_num, course_name=course_name).first()

            if marks is not None:
                student_name = Student.objects.get(id_num=id_num)
                edit_mark_form = CreateMarkForm(
                    initial={'class_activity': marks.class_activity,
                             'quizzes': marks.quizzes,
                             'midterm': marks.midterm,
                             'final': marks.final,
                             'extra_mark': marks.extra_mark,
                             'total_mark': marks.total_mark,
                             'description': marks.description,
                             }
                )
                full_Name = f'{student_name.first_name} {student_name.last_name}'
                context['full_name'] = full_Name
                context["class_name"] = course_name.title

                context['form'] = edit_mark_form
                context['student_flag'] = False
                context['course_flag'] = False
                context['mark_flag'] = True
            else:
                context['mark_flag'] = False
                context['student_flag'] = False
                context['course_flag'] = True

                messages.error(request, "نمره برای این دانش آموز ثبت نگردیده است")

        if 'ارسال' in request.POST:

            edit_mark_form = CreateMarkForm(request.POST)

            if edit_mark_form.is_valid():
                class_activity = edit_mark_form.cleaned_data['class_activity']
                midterm = edit_mark_form.cleaned_data['midterm']
                final = edit_mark_form.cleaned_data['final']
                quizzes = edit_mark_form.cleaned_data['quizzes']
                extra_mark = edit_mark_form.cleaned_data['extra_mark']
                total_mark = edit_mark_form.cleaned_data['total_mark']
                total_work = request.POST['total_work']
                description = edit_mark_form.cleaned_data['description']
                writing = request.POST['writing']
                homework = request.POST['homework']
                listening = request.POST['listening']
                speaking = request.POST['speaking']
                activity = request.POST['activity']
                student_name = Student.objects.get(id_num=id_num)

                y = Mark.objects.filter(student_name=student_name, course_name=course_name).first()
                y.delete()
                x = Mark.objects.create(student_name=student_name, course_name=course_name,
                                        class_activity=class_activity,
                                        quizzes=quizzes, midterm=midterm, final=final,
                                        extra_mark=extra_mark, total_mark=total_mark,
                                        total_work=total_work,
                                        description=description, activity=activity,
                                        speaking=speaking, listening=listening,
                                        writing=writing, homework=homework,
                                        )

                x.save()
                messages.success(request, "نمرات با موفیقت ویرایش شد")
                return redirect('/edit-mark')

    user_id = request.user.username

    teacher = TeacherClass.objects.filter(id_num=user_id).first()

    course = Course.objects.filter(teacher=teacher, active=True)
    context['course'] = course

    return render(request, 'edit_mark_page.html', context)


@login_required(login_url='/login')
def final_report(request, *args, **kwargs):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Student':
        return redirect('/')
    context = {}
    id_num = request.user.username
    course_name = Course.objects.get(id=kwargs['course_id'])

    marks = Mark.objects.filter(student_name__id_num=id_num, course_name=course_name).first()
    context['teacher'] = marks.teacher if marks.teacher is not None else course_name.teacher
    pre_marks = Mark.objects.filter(student_name__id_num=id_num).order_by('course_name')
    if marks is not None:
        context['activity'] = get_mark_value(marks.activity)
        context['speaking'] = get_mark_value(marks.speaking)
        context['listening'] = get_mark_value(marks.listening)
        context['writing'] = get_mark_value(marks.writing)
        context['homework'] = get_mark_value(marks.homework)

        context['total_work'] = get_mark_value(marks.total_work)

        mean = context['activity'] + context['speaking'] + context['listening'] + context['writing'] + context[
            'homework'] + context['total_work']
        context['mean'] = mean / 6

        context['marks'] = marks
        full_Name = UserProfile.objects.get(user=request.user).full_name
    else:
        context['marks'] = None
        full_Name = UserProfile.objects.get(user=request.user).full_name

    context['full_name'] = full_Name
    context['pre_marks'] = pre_marks
    return render(request, 'final_report.html', context)


def get_mark_value(mark: str) -> int:
    if mark == 'Out_Standing':
        return 100
    elif mark == 'Good':
        return 75
    elif mark == 'Satisfactory':
        return 50
    elif mark == 'Weak':
        return 25
