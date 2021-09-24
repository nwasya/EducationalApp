from django.shortcuts import render

# Create your views here.
from Edu_register.forms import CreateRegisterForm
from Edu_register.models import Register


def register_page(request):
    register_form = CreateRegisterForm(request.POST or None)

    if request.method == 'POST':
        full_name = request.POST['full_name']
        id_num = request.POST['id_num']
        phone = request.POST['phone_num']
        latest_course = request.POST['latest_course']
        address = request.POST['address']
        birth = request.POST['birth']
        description = request.POST['text']

        Register.objects.create(full_name=full_name, id_num=id_num, phone=phone,
                                latest_course=latest_course, address=address, birth=birth,
                                description=description, is_read=False)

        # todo : show user a success message

        register_form = CreateRegisterForm()



    context = {
        'register_form': register_form,

    }
    return render(request, 'register/register_page.html', context)
