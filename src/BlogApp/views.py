from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import author, article, category
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

# Create your views here.
# User login and singup or contact section start
def userRegister(request):
	templete_name = 'account/register.html'
	return render(request, templete_name)

def userLogin(request):
	form = CreateUserForm()

	templete_name = 'account/login.html'
	return render(request, templete_name)

def userContact(request):
	templete_name = 'account/contact.html'
	return render(request, templete_name)
	
# User login and singup or contact section End

# Main content start
def homeView(request):
	post=article.objects.all
	templete_name = 'index.html'
	context = {
		'post': post
	}
	return render(request, templete_name, context)

def blogView(request):
	blogPost = article.objects.all
	templete_name = 'blog.html'
	context={
		'blogPost': blogPost
	}
	return render(request, templete_name, context)

def postView(request, id):
	post          = get_object_or_404(article, id=id)
	firstPost     = article.objects.first()
	lastPost 	  = article.objects.last
	related		  = article.objects.filter(category=post.category).exclude(id=id)[:3]
	templete_name = 'post.html'
	context={
		'post': post,
		'firstPost': firstPost,
		'lastPost': lastPost,
		'related':  related
	}
	return render(request, templete_name, context)

def userAccount(request):
	author_post = get_object_or_404(author)
	templete_name = 'account/account.html'
	context={
		'author_post': author_post
	}
	return render(request, templete_name, context)

def postCategory(request, name):
	cat = get_object_or_404(category, name=name)
	templete_name = 'category.html'
	post = article.objects.filter(category=cat.id)
	context={
		'post': post,
		'cat': cat
	}
	return render(request, templete_name, context)

