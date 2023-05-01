from django.urls import path  
from django.contrib import admin
from django.conf import settings 
from django.urls import path
from django.conf.urls.static import static 
from .views import *
from .models import *

app_name = 'blog'  
  
urlpatterns = [  
    path('', post_list, name='post_list'),  
    path('<int:id>', post_detail,  name='post_detail'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)