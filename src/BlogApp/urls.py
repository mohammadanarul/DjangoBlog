from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
# from . import views
from .views import (
    userRegister,
    userLogin,
    userLogOut,
	homeView,
	blogView,
	postView,
    userContact,
    makeUserProfile,
    postCategory,
    createPost,
    upDatePost,
    deletePost,
    userProfilePost
)
app_name = 'BlogApp'
urlpatterns = [
    # path('', homeView),
    path('', homeView, name='home'),
    path('post/<int:id>/', postView, name='post'),
    path('blog/', blogView, name='BlogPost'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('userlogout/', userLogOut, name='logOut'),
    path('contact/', userContact, name='contact'),
    path("profile/", makeUserProfile, name='userProfile'),
    path('<name>/', userProfilePost, name='userPost'),
    path('postcategory/<name>/', postCategory, name='category'),
    path('createPost', createPost, name='ceartePost'),
    path('update/<int:pk>/', upDatePost, name='update'),
    path('delete/<int:pk>/', deletePost, name='deletePost'),
]

if settings.DEBUG:
    # test mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
