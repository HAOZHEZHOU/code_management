from __future__ import unicode_literals
from django.template import loader,Context
from django.http import HttpResponse
from manager.base.models import user,user_role,user_group,audit_log
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import hashlib
__author__ = 'zhouhaozhe'
class LocalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(LocalEncoder, self).default(obj)

def log_list(request):
    if request.method == 'POST':
        start = request.POST['iDisplayStart']
        begin = int(start)
        length = request.POST['iDisplayLength']
        end = int(length) + int(start)
        logs = audit_log.objects.all()
        aData = logs[begin:end]
        aData = json.loads(serializers.serialize("json", aData, cls=LocalEncoder))
        response_data = {"data": aData, "recordsTotal": len(logs), "recordsFiltered": len(logs)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render_to_response('pages/base/audit_log_list.html',{'request':request,'username':request.session['user_name']})
