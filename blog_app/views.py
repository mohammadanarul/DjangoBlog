from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import author, article, category, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CreateUserForm, createUserPost, createUserProfile, userCommentForm, createCategoryForm
from django.contrib import messages
from django.db.models import Q, Count 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .tokens import userAccountRegisterActiveTokenGenerate

# Create your views here

def userContact(request):
	templete_name = 'account/contact.html'
	return render(request, templete_name)

# User login and singup or contact section End

# Main content start
def baseView(request):
	post = article.objects.all()
	recentPost = article.objects.filter(published=True).order_by('-posted_on')[0:3]
	search   = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search) 
		)
	template_name = 'base.html'
	context={
		'post': post,
		'recentPost': recentPost,
	}
	return render(request, template_name, context)
def homeView(request):
	post = article.objects.all();
	recentPost = article.objects.filter(published=True).order_by('-posted_on')[0:3]
	recentimage = article.objects.filter(published=True).order_by('-posted_on')[0:4]
	search   = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search) 
		)
	# paginator = Paginator(post, 3)
	# page = request.GET.get('page')
	# page_list = paginator.get_page(page)
	templete_name = 'index.html'
	context = {
		'post': post,
		'recentPost': recentPost,
		'recentimage': recentimage,
	}
	return render(request, templete_name, context)

def blogView(request):
	post = article.objects.all()
	recentPost = article.objects.filter(published=True).order_by('-posted_on')[0:4]
	# category_list_count = article.objects.annotate(num_category=Count('category'))[0:5]
	categories = category.objects.all().annotate(posts_count=Count('article'))
	comments = Comment.objects.filter(post=post).order_by('-id')

	search   = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title__icontains=search) |
			Q(body__icontains=search) 
		)
	paginator = Paginator(post, 4)
	page = request.GET.get('page')
	page_list = paginator.get_page(page)
	templete_name = 'blog.html'
	context={
		'post': page_list,
		'recentPost': recentPost,
		'categories': categories,
		'comments': comments,
	}
	return render(request, templete_name, context)

def postView(request, id):
	post     	  = get_object_or_404(article, id=id)
	firstPost     = article.objects.first()
	lastPost 	  = article.objects.last()
	related		  = article.objects.filter(category=post.category).exclude(id=id)[0:4]
	blogPostViewCount = article.objects.get(id=id)
	blogPostViewCount.blog_post_views = blogPostViewCount.blog_post_views+1
	blogPostViewCount.save()
	comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
	categories = category.objects.all().annotate(posts_count=Count('article'))
	templete_name = 'post.html'
	if request.method == 'POST':
		comment_form = userCommentForm(request.POST or None)
		if comment_form.is_valid:
			post_comment = request.POST.get('post_comment')
			reply_id = request.POST.get('comment_id')
			comment_qs = None
			if reply_id:
				comment_qs = Comment.objects.get(id=reply_id)
			comment = Comment.objects.create(post=post, user=request.user, post_comment=post_comment, reply=comment_qs)
			comment.save()
			return redirect('blog:post', id=post.id)
	else:
		comment_form = userCommentForm()
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		is_liked = True

	context={
		'post': post,
		'firstPost': firstPost,
		'lastPost': lastPost,
		'related':  related,
		'viewCount': blogPostViewCount,
		'categories': categories,
		'comments': comments,
		'comment_form': comment_form,
		'is_liked': is_liked,
	}
	return render(request, templete_name, context)

def post_like(request):
	post = get_object_or_404(article, id=request.POST.get('article_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True
	return redirect('blog:post', id=post.id)


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
				return redirect('blog:create-user-profile')
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
	recentPost = article.objects.filter(published=True).order_by('-posted_on')[0:4]
	categories = category.objects.all().annotate(posts_count=Count('article'))
	paginator = Paginator(post, 4)
	page = request.GET.get('page')
	page_list = paginator.get_page(page)
	template_name = 'account/userPost.html'
	context={
		'auth': auth,
		'post': page_list,
		'recent_post': recentPost,
		'category': categories,
	}
	return render(request, template_name, context)

def postCategory(request, name):
	cat = get_object_or_404(category, name=name)
	post = article.objects.filter(category=cat.id)
	recentPost = article.objects.filter(published=True).order_by('-posted_on')[0:4]
	categories = category.objects.all().annotate(posts_count=Count('article'))
	# blogPostViewCount = article.objects.get(id=id)
	# blogPostViewCount.blog_post_views = blogPostViewCount.blog_post_views+1
	# blogPostViewCount.save()
	paginator = Paginator(post, 4)
	page = request.GET.get('page')
	page_list = paginator.get_page(page)
	templete_name = 'category.html'
	context={
		'post': page_list,
		'cat': cat,
		'recent': recentPost,
		'cats': categories,
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
			return redirect('blog:profile')
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
			return redirect('blog:profile')
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

def our_services(request):
	templete_name = 'our_services.html'
	return render(request, templete_name)

def profile(request):
	if request.user.is_authenticated:
		user			= get_object_or_404(User, id=request.user.id)
		userProfile 	= author.objects.filter(name=user.id)
		templete_name   = 'account/profile.html'
		if userProfile:
			userAuthor  = get_object_or_404(author, name=request.user.id)
			userPost 	= article.objects.filter(article_author=userAuthor.id)
			paginator = Paginator(userPost, 4)
			page = request.GET.get('page')
			page_list = paginator.get_page(page)
			context ={
				'post': page_list,
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
				return redirect('blog:profile')
			context={
				'form': form
			}
			return render(request, templete_name, context)
	else:
		return redirect('blog:login')
def aboutView(request):
	templete_name = 'about.html'
	return render(request, templete_name)

def createCategoryView(request):
	form = createCategoryForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return redirect('blog:profile')
	template_name = 'createCategory.html'
	context ={
		'form': form
	}
	return render(request, template_name, context)

def blog_search(request):
	post = article.objects.all()
	search = request.GET.get('q')
	if search:
		post=post.filter(
			Q(title_icontains=search) |
			Q(body_icontains=search)
		)
	template_name = 'blog_search.html'
	context= {
		'post': post,
	}
	return render(request, template_name, context)

def footer_recent_post(request):
	post = get_object_or_404(article)
	recent_footer_post = article.objects.filter(published=True).order_by('-posted_on')[0:4]
	template_name= 'footer_recent_post.html'
	context = {
		'recent_footer_post': post,
	}
	return render(request, template_name, context)

# Django default language English 

def switch_to_bangla_link(request):
	request.session['lang'] = 'bangla'
	return render(request, 'test.html')
# userAuthor = get_object_or_404(author, name=request.user.id)
# 	userPost = article.objects.filter(article_author=userAuthor.id)
# 	templete_name = 'account/profile.html'
# 	paginator = Paginator(userPost, 4)
# 	page = request.GET.get('page')
# 	page_list = paginator.get_page(page)
# 	context = {
# 		'post': page_list,
# 		'userAuthor': userAuthor,
# 	}
# 	return render(request, templete_name, context)