from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_of_post, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.list_of_post_by_category, name='list_of_post_by_category')

]
