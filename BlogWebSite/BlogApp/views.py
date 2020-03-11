from django.shortcuts import render, HttpResponse

# Create your views here.
def homeView(request):
	return render(request, 'index.html')

def blogView(request):
	return render(request, 'blog.html')

def postView(request):
	return render(request, 'post.html')