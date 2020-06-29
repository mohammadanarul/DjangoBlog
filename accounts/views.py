from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib import messages
from django.db.models import Q, Count 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .tokens import userAccountRegisterActiveTokenGenerate

# Create your views here
# User login and singup or contact section start
def userRegister(request):
	if request.user.is_authenticated:
		return redirect('/home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.is_active = False
				instance.save()
				site = get_current_site(request)
				mail_subject = 'Actiavte your account'
				message = render_to_string('accounts/confirm.html',{
					'user': instance,
					'domain': site.domain,
					'uid': instance.id,
					'token': userAccountRegisterActiveTokenGenerate.make_token(instance),
				})
				to_email = form.cleaned_data.get('email')
				to_list = [to_email]
				from_email = settings.EMAIL_HOST_USER
				send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
				return HttpResponse('<h1>Thanks for your registration. A confirmation link was sent to your email.</h1>')
		context	={
			'form': form,
		}
		return render(request, 'accounts/register.html', context)

def userAccountActivate(request, uid, token):
	try:
		user = get_object_or_404(User, pk=uid)
	except:
		raise Http404('User is not valite')

	if user is not None and userAccountRegisterActiveTokenGenerate.check_token(user, token):
		user.is_active = True
		user.save()
		return HttpResponse("<h1>Your Blog account activated. Now you can <a href='{% url 'blog:login' %}'>login</a></h1>")
	else:
		return HttpResponse('<h1>Your Activation link is Not invalid.</h1>')