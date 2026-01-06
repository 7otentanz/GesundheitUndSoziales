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
    path('start/', app.start),
    path('terminspezialisierung/', app.terminspezialisierung, name="terminspezialisierung"),
    path('terminstandort/', app.terminstandort, name="terminstandort"),
    path('terminarzt/', app.terminarzt, name="terminarzt"),
    path('termintest/', app.termintest, name="termintest"),
]
urlpatterns += staticfiles_urlpatterns()
