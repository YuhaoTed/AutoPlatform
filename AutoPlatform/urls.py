"""AutoPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from Automation import views
from django.views.static import serve
from AutoPlatform import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('index/',views.index),
    path('reg/',views.reg),
    path('manage/',views.manage_user),
    re_path('auth_user/([0-9]+)/', views.auth_user),#/auth_user/{{user.nid}}
    re_path('delete_user/([0-9]+)/', views.del_user),
    re_path('delete_function/([0-9]+)/', views.del_function),
    re_path('addcase/([0-9]+)/', views.addcase),
    re_path('^$',views.index),
    path('Function_add/',views.Function_add),
    path('FeatureList/', views.featurelist),
    path('CaseList/',views.caselist),
    path('addsds/',views.addsds),
    path('addicon/',views.addicon),
    path('sdslist/',views.sdslist),
    path('iconlist/',views.iconlist),
    re_path(r"media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT})

]
