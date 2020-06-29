from django.contrib import admin
from django.urls import include, path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from covid19.views import covid_19_Views
from weather.views import weather


urlpatterns = [
    path('pfe/', admin.site.urls),
    path('', include('blog_app.urls', namespace='blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('covid-19-live-scoure', covid_19_Views, name='covid-19-live-scoure'),
    path('weather', weather, name='weather'),
    path('register', accounts_views.userRegister, name='register'),
    path('activate/<uid>/<token>', accounts_views.userAccountActivate, name='activate'),
    path('login', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]
