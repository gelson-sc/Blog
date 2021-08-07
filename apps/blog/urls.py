from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_of_post, name='list_of_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.list_of_post_by_category, name='list_of_post_by_category')

]
