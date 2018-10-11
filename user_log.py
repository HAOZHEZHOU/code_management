# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from manager.base.models import audit_log
import datetime
from django.conf import urls,settings
import json
import os
__author__ = 'zhouhaozhe'
class Middlel(MiddlewareMixin):
    def process_response(self,request,response):
        try:
            remote_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            remote_ip = request.META['REMOTE_ADDR']

        home = settings.STATIC_ROOT
        if os.path.exists(home+request.path):
            return response
        print request.path
        try:
            user_name = request.session['user_name']
            role_name = request.session['user_role']
        except KeyError:
            user_name = "chengpu script"
            role_name = "none"
        audit_log.objects.create(user_name=user_name,
                                 role_name = role_name,
                                 ip=remote_ip,
                                 uri = request.path,
                                 method = request.method,
                                 params = '{"GET":'+json.dumps(request.GET)+',"POST":'+json.dumps(request.POST)+'}',
                                 status_code = response.status_code,
                                 insert_time = datetime.datetime.now(),
                                 handler = 'zhouhaozhe',
                                 handle_time = datetime.datetime.now(),
                                 )
        print 'filter is done'
        return response

