from django.conf.urls import url
from manager.base.views.login import *
from manager.base.views.index import *
from manager.base.views.message import *
__author__ = 'zhouhaozhe'

urlpatterns=[
            url(r'^login/$',login),
            url(r'^$',login),
            url(r'^add_user',add_user),
            url(r'^del_user',remove_user),
            url(r'^user_list',user_list),
            url(r'^group_add',add_group),
            url(r'^group_del',remove_group),
            url(r'^group_list',group_list),
            url(r'^message_list',message_list),
            url(r'^add_message',add_message),
            url(r'^read_message',read_message),
            url(r'^message',message),
            url(r'^new_message_count',new_message_count),
            url(r'^send_message',send_message),
            url(r'^log_list',log_list),
            url(r'^logout',logout),
            ]