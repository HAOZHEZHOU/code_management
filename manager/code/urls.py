from django.conf.urls import url

from manager.code.views.code import *
from manager.code.views.project import *

__author__ = 'zhouhaozhe'

urlpatterns=[
            url(r'^upload_code',upload_code),
            url(r'^del_code',del_code),
            url(r'^add_project',add_project),
            url(r'^del_project',del_project),
            url(r'^edit_project',edit_project),
            url(r'^project_list',project_list),
            url(r'code_timeline',code_timeline),
            url(r'code_diff',code_diff),
            url(r'use_old',use_old),
            url(r'edit_new',edit_new),
            url(r'^upload_code',upload_code),

          ]