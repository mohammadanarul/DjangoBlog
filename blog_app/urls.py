from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog_app.views import (
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
    userProfilePost,
    our_services,
    profile,
    aboutView,
    createCategoryView,
    post_like,
    switch_to_bangla_link,
)
app_name = 'blog_app'
urlpatterns = [
    path('', homeView, name='home'),
    path('post/<int:id>/', postView, name='post'),
    path('blog/', blogView, name='BlogPost'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('userlogout/', userLogOut, name='logOut'),
    path('contact/', userContact, name='contact'),
    path("create-user-profile/", makeUserProfile, name='create-user-profile'),
    path('user-post/<name>/', userProfilePost, name='user-post'),
    path('post-category/<name>/', postCategory, name='category'),
    path('create-post/', createPost, name='ceartePost'),
    path('update/<int:pk>/', upDatePost, name='update'),
    path('delete/<int:pk>/', deletePost, name='deletePost'),
    path('profile/', profile, name='profile'),
    path('our-services/', our_services, name='our-services'),
    path('about/', aboutView, name='about'),
    path('create-category', createCategoryView, name='create-category'),
    path('likes', post_like, name='likes'),
    path('language', switch_to_bangla_link, name='language'),
]

if settings.DEBUG:
    # test mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
