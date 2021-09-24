from django.shortcuts import render

# Create your views here.
from Edu_contact.forms import CreateContactForm
from Edu_contact.models import ContactUs


def contact_page(request):
    contact_form = CreateContactForm(request.POST or None)

    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        subject = request.POST['subject']
        text = request.POST['text']
        print(full_name,email,text,subject)

        ContactUs.objects.create(full_name=full_name, email=email, subject=subject, text=text, is_read=False)

        # todo : show user a success message

        contact_form = CreateContactForm()



    context = {
        'contact_form': contact_form,

    }
    return render(request, 'contact_us/contact_us_page.html', context)
