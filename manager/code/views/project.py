from __future__ import unicode_literals
from django.template import loader,Context
from django.http import HttpResponse
from manager.code.models import project
from manager.base.models import user
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from datetime import datetime
__author__ = 'zhouhaozhe'

class LocalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(LocalEncoder, self).default(obj)

def add_project(request):
    if request.method == 'POST':
        project_owner = request.POST.get('project_owner')
        project_name = request.POST.get('project_name')
        project_intro = request.POST.get('project_intro')
        project_owner = project_owner.split(',')
        for user_one in project_owner:
            user_tmp = user.objects.filter(id=user_one)
            user_tmp.update(project_name = project_name)
        project.objects.create(project_owner = project_owner,
                               project_name = project_name,
                               project_intro = project_intro,
                               project_creator = request.session['user_name'])
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")
    else:
        print '222'

def edit_project(request):
    print "rr"

def del_project(request):
    project_name = request.POST.get('project_name')
    project.objects.filter(project_name=project_name).delete()
    user.objects.filter(project_name=project_name).update(project_name='')
    return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")

def project_list(request):
    if request.method == 'POST':
        start = request.POST['iDisplayStart']
        begin = int(start)
        length = request.POST['iDisplayLength']
        end = int(length) + int(start)
        projects = project.objects.all()
        aData = projects[begin:end]
        aData = json.loads(serializers.serialize("json", aData, cls=LocalEncoder))
        response_data = {"data": aData, "recordsTotal": len(projects), "recordsFiltered": len(projects)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        user_list = user.objects.filter(project_name='')
        return render_to_response('pages/code/project_list.html',{'request':request,'user':user_list,'username':request.session['user_name']})