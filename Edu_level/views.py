from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from Edu_level.forms import CreateLevelForm, EditLevelForm
from Edu_level.models import Level
from Edu_user.models import UserProfile


def levels_detail(request, *args, **kwargs):
    selected_level_id = kwargs['levelId']
    level = Level.objects.get(id=selected_level_id)

    if level is None:
        raise Http404('کلاس مورد نظر یافت نشد')
    context = {
        'product': level,

    }
    return render(request, 'levels_detail.html', context)


@login_required(login_url='/login')
def add_level(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        level_form = CreateLevelForm(request.POST, request.FILES)
        if level_form.is_valid():
            title = level_form.cleaned_data.get('title')
            description = level_form.cleaned_data.get('description')
            short_description = level_form.cleaned_data.get('short_description')
            image = request.FILES['image']
            level_model = Level(title=title, description=description, image=image,short_description=short_description
                                )

            level_model.save()
            return redirect('add-level')

    level_form = CreateLevelForm()

    context = {

        'form': level_form,

    }
    return render(request, 'add_level.html', context)


@login_required(login_url='/login')
def delete_level(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')
    if request.method == 'POST':
        level_id = request.POST['dropdown']
        if level_id != None:
            Level.objects.get(id=level_id).delete()
            return redirect('/delete-level')

    level_list = Level.objects.all()
    context = {
        'level_list': level_list
    }
    return render(request, 'delete_level.html', context)



li = []
@login_required(login_url='/login')
def edit_level(request):
    if UserProfile.objects.get(user__username=request.user.username).role != 'Manager':
        return redirect('/')


    context = {}
    context['confirm'] = False

    if request.method == 'POST':

        if 'جستجو' in request.POST:

            level_id = request.POST.get('dropdown')

            li.append(level_id)
            context['level_id'] = level_id
            if level_id != None:
                level_obj = Level.objects.get(id=level_id)
                edit_level_form = EditLevelForm(
                    initial={'title': level_obj.title,
                             'description': level_obj.description}
                )

                if level_obj is None:
                    return Http404
                else:
                    context['edit_form'] = edit_level_form
                    context['confirm'] = True

        if 'ذخیره' in request.POST:

            level_id_num = li[-1]
            edit_level_form = EditLevelForm(request.POST)
            level_obj = Level.objects.get(id=level_id_num)

            if edit_level_form.is_valid():
                title = edit_level_form.cleaned_data.get('title')
                description = edit_level_form.cleaned_data.get('description')
                short_description = edit_level_form.cleaned_data.get('short_description')



                level_obj.title = title
                level_obj.description = description
                level_obj.short_description = short_description

                level_obj.save()
                return redirect('/edit-level')

    level_list = Level.objects.all()

    context['level_list'] = level_list

    return render(request, 'edit_level.html', context)
