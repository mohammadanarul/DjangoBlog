from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
# from . import views
from .views import (
    userRegister,
    userLogin,
	homeView,
	blogView,
	postView,
    userContact,
    userAccount,
   postCategory
)
app_name = 'blog'
urlpatterns = [
    # path('', homeView),
    path('', homeView, name='home'),
    path('post/<int:id>/', postView, name='post'),
    path('blog/', blogView, name='BlogPost'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('contact/', userContact, name='contact'),
    path("profile/", userAccount, name='account'),
    path('postcategory/<name>/', postCategory, name='category')
]

if settings.DEBUG:
    # test mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
