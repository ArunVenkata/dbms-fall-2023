# coding=utf-8

from django.urls import re_path as url, path

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add),
    url(r'^edit/$', views.edit),
    url(r'^delete/$', views.delete)
    # url('add', views.add),
    # url('edit', views.edit),
    # url('delete', views.delete)
]

# urlpatterns = [
# url('/', views.index),
#     path('add', views.add_view),
#     path('delete', views.delete_view),
#     path('edit', views.edit_view),
#     # 添加其他URL模式
# ]