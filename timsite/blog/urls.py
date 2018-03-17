from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('archives/', views.archives, name='archives'),
    path('blog/<slug:slug>/', views.page, name='post'),
]
