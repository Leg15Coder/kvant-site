"""kvant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include  
from django.contrib import admin  
from blog.models import *
from blog import views
  
urlpatterns = [  
    path('', views.home, name='home'),
    path('', include('blog.urls')), 

    path('admin/', admin.site.urls),

    path('profile/<str:user>/', views.profile_user_view, name='profile'),
    path('login/', views.LoginUserView.as_view(), name="login_page"),  
    path('logout/', views.LogoutSys.as_view(), name="logout_page"),
    path('register/', views.register, name="register"),
    path('activation_code_form/', views.endreg, name="endreg"),
    
    path('posts/<str:type>/', views.post_list, name="post_list"), 
    path('posts/<int:year>/<int:month>/<int:day>/', views.post_detail,  name='post_detail'),  

    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('dialogs/<int:chat_id>/', views.MessagesView.as_view(), name='messages'),

    path('groups/', views.CreateGroupView.as_view(), name="studentgroups"),
    #path('groups/', views.GroupsView.as_view(), name="studentgroups"),
    path('groups/<int:id>/', views.GroupsView.as_view(), name="group_detail"),

    path('info/<str:type>/', views.info, name="info"),

    path('', include('social_django.urls')),
]