from django.shortcuts import render,redirect
from django.views.generic import ListView

from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from Edu_news.forms import CreateNewsForm, EditNewsForm
from Edu_news.models import News
from Edu_user.models import UserProfile


class NewsPage(ListView):
    template_name = 'news_page.html'

    paginate_by = 6


    def get_queryset(self):
        return News.objects.all().order_by('id').reverse()


li = []
@login_required(login_url='/login')
def create_news_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role == 'Manager':
        pass
    elif UserProfile.objects.get(user__username=request.user.username).role == 'Teacher':
        pass
    else:
        return redirect('/')
    if request.method == 'POST':
        news_form = CreateNewsForm(request.POST, request.FILES)
        if news_form.is_valid():
            title = news_form.cleaned_data.get('title')
            text = news_form.cleaned_data.get('text')
            user_name = request.user.profile.full_name
            value = request.FILES.get('image')
            if value:
                image = request.FILES['image']
                news_model = News(title=title, text=text,image=image, user_name=user_name, active=True)
            else:
                news_model = News(title=title, text=text, user_name=user_name, active=True)


            news_model.save()
            messages.success(request,f'خبر با موضوع {str(title)} با موفقیت ثبت شد.')
            return HttpResponseRedirect('/addnews')
        else:
            messages.error(request,'ثبت خبر با خطا مواجه شد.')

    news_form = CreateNewsForm()
    context = {

        'form': news_form

    }
    return render(request, 'add_news.html', context)

@login_required(login_url='/login')
def edit_news_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role == 'Manager':
        pass
    elif UserProfile.objects.get(user__username=request.user.username).role != 'Teacher':
        pass
    else:
        return redirect('/')
    context = {}
    context['confirm'] = False

    if request.method == 'POST':

        if 'جستجو' in request.POST:

            news_id_num = request.POST.get('dropdown')

            li.append(news_id_num)
            context['news_id_num'] = news_id_num
            news_obj = News.objects.get(id=news_id_num)

            edit_news_form = EditNewsForm(
                initial={'title': news_obj.title,
                         'text': news_obj.text,
                         }
            )

            if news_obj is None:

                messages.error(request,'خبر مورد نظر یافت نشد')
            else:
                context['edit_form'] = edit_news_form
                context['confirm'] = True

        if 'ذخیره' in request.POST:

            news_id_num = li[-1]
            edit_news_form = EditNewsForm(request.POST)
            news_obj = News.objects.get(pk=news_id_num)

            if edit_news_form.is_valid():
                text = edit_news_form.cleaned_data.get('text')
                title = edit_news_form.cleaned_data.get('title')

                news_obj.text = text
                news_obj.title = title


                news_obj.save()
                messages.success(request,'خبر با موفقیت ویرایش شد.')
                return redirect('/editnews')
            else:
                messages.error(request,'ویرایش خبر با خطا مواجه شد.توجه داشته باشید که موضوع خبر نباید بیش از 150 کاراکتر باشد')

    news_list = News.objects.filter(user_name=request.user.profile.full_name).order_by('-id')

    context['news_list'] = news_list

    return render(request, 'edit_news_page.html', context)


@login_required(login_url='/login')
def delete_news_page(request):
    if UserProfile.objects.get(user__username=request.user.username).role == 'Manager':
        pass
    elif UserProfile.objects.get(user__username=request.user.username).role == 'Teacher':
        pass
    else:
        return redirect('/')

    if request.method == 'POST':
        new = request.POST['dropdown']

        News.objects.filter(id=new).delete()
        messages.success(request, 'خبر با موفقیت حذف شد.')

    news_list = News.objects.filter(user_name=request.user.profile.full_name)
    context = {
        'news_list': news_list
    }
    return render(request, 'delete_news.html', context)

