"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as app
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jwt-login', app.jwt_login),
    path('start/', app.start, name='start'),
    path('elterngeldberechtigte/', app.elterngeldberechtigte),
    path('elterngeldanlegen', app.elterngeldanlegen),
    path('kindergeldberechtigte/', app.kindergeldberechtigte),
    path('kindergeldanlegen', app.kindergeldanlegen),
    path('api_rentenbetraege/', app.api_rentenbetraege),
    path('api_arbeitslosenbetraege/', app.api_arbeitslosenbetraege),
    path('api_sozialleistungen/<str:user_id>', app.api_sozialleistungen, name = 'sozialleistungen'),
    path('sozialleistungen/', app.sozialleistungen, name='sozialleistungen'),
    

]
urlpatterns += staticfiles_urlpatterns()
