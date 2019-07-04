from django.conf.urls import include, url
from django.contrib import admin

from login import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),  # 显示登录页面
    url(r'^login_check$', views.login_check),  # 登录校验页面
    url(r'^main$', views.main),  # 登录成功后，显示登录主页面
    url(r'^ajax_test$', views.ajax_test),  # 显示ajax测试页面
    url(r'^ajax_handler$', views.ajax_handler),  # 处理ajax请求
    url(r'^change_pwd$', views.change_pwd),  # 显示修改密码页面
    url(r'^handler_change_pwd$', views.handler_change_pwd),  # 处理修改密码
]
