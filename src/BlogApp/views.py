from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import author, article, category, comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CreateUserForm, createUserPost, createUserProfile, userCommentForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.
# User login and singup or contact section start
def userRegister(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Welcome to ' + user +' Your blog account has been successfully created')
			return redirect('blog:login')

	templete_name = 'account/register.html'
	context={
		'form': form
	}
	return render(request, templete_name, context)

def userLogin(request):
	if request.user.is_authenticated:
		return redirect('blog:home')
	else:
		if request.method == 'POST':
			user = request.POST.get('username')
			password = request.POST.get('password')
			auth = authenticate(request, username=user, password=password)
			if auth is not None:
				login(request, auth)
				return redirect('blog:home')
			else:
				messages.info(request, 'Your Username Or Password is incorrect')
		templete_name = 'account/login.html'
	return render(request, templete_name)
def userLogOut(request):
	logout(request)
	return redirect('blog:home')

def userContact(request):
	templete_name = 'account/contact.html'
	return render(request, templete_name)

# User login and singup or contact section End

# Main content start
def homeView(request):
	post = article.objects.all();
	search   = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search) 
		)
	paginator = Paginator(post, 2)
	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	templete_name = 'index.html'
	context = {
		'contacts': contacts
	}
	return render(request, templete_name, context)

def blogView(request):
	post = article.objects.all()
	search   = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search) 
		)
	templete_name = 'blog.html'
	context={
		'post': post
	}
	return render(request, templete_name, context)

def postView(request, id):
	post     = get_object_or_404(article, id=id)
	firstPost     = article.objects.first()
	lastPost 	  = article.objects.last()
	related		  = article.objects.filter(category=post.category).exclude(id=id)[:3]
	userComment   = comment.objects.filter(post=id)
	form 		  = userCommentForm(request.POST or None)
	templete_name = 'post.html'
	if form.is_valid():
		instance = form.save(commit=False)
		instance.post=post
		instance.save()
		return redirect('blog:post', id=post.id)

	context={
		'post': post,
		'firstPost': firstPost,
		'lastPost': lastPost,
		'related':  related,
		'form': form,
		'comment': userComment
	}
	return render(request, templete_name, context)

def makeUserProfile(request):
	if request.user.is_authenticated:
		user			= get_object_or_404(User, id=request.user.id)
		userProfile 	= author.objects.filter(name=user.id)
		templete_name   = 'account/account.html'
		if userProfile:
			userAuthor  = get_object_or_404(author, name=request.user.id)
			userPost 	= article.objects.filter(article_author=userAuthor.id)
			context ={
				'userPost': userPost,
				'userAuthor': userAuthor
			}
			return render(request, templete_name, context)
		else:
			form = createUserProfile(request.POST or None, request.FILES or None)
			templete_name = 'account/authorForm.html'
			if form.is_valid():
				instance = form.save(commit=False)
				instance.name=user
				instance.save()
				return redirect('blog:userProfile')
			context={
				'form': form
			}
			return render(request, templete_name, context)
	else:
		return redirect('blog:login')

def userProfilePost(request, name):
	userPost = get_object_or_404(User, username=name)
	auth     = get_object_or_404(author, name=userPost.id)
	post     = article.objects.filter(article_author=auth.id)
	template_name = 'account/userPost.html'
	context={
		'auth': auth,
		'post': post
	}
	return render(request, template_name, context)

def postCategory(request, name):
	cat = get_object_or_404(category, name=name)
	post = article.objects.filter(category=cat.id)
	templete_name = 'category.html'
	context={
		'post': post,
		'cat': cat
	}
	return render(request, templete_name, context)

def createPost(request):
	if request.user.is_authenticated:
		user = get_object_or_404(author, name=request.user.id)
		postForm = createUserPost(request.POST or None, request.FILES or None)
		templete_name = 'createPost.html'
		context={
			'form': postForm
		}
		if postForm.is_valid():
			instance = postForm.save(commit=False)
			instance.article_author = user
			instance.save()
			messages.success(request, 'Your Posted succesfully')
			return redirect('blog:userProfile')
		return render(request, templete_name, context)
	else:
		return redirect('blog:home')

def upDatePost(request, pk):
	if request.user.is_authenticated:
		user 	 = get_object_or_404(author, name=request.user.id)
		post 	 = get_object_or_404(article, id=pk)
		postForm = createUserPost(request.POST or None, request.FILES or None, instance=post)
		templete_name = 'createPost.html'
		if postForm.is_valid():
			instance = postForm.save(commit=False)
			instance.article_author = user
			instance.save()
			messages.success(request, 'Your post has been updated successfully')
			return redirect('blog:userProfile')
		context={
			'form': postForm
		}
		return render(request, templete_name, context)
	else:
		return redirect('blog:home')

def deletePost(request, pk):
	if request.user.is_authenticated:
		post = get_object_or_404(article, id=pk)
		post.delete()
		messages.warning(request, 'Your post has been updated successfully')
		return redirect('blog:userProfile')
	else:
		return redirect('blog:login')

