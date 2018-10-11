from __future__ import unicode_literals
from django.template import loader,Context
from django.http import HttpResponse
from manager.base.models import user
from manager.code.models import project,file
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.files.base import ContentFile
from django.shortcuts import render,render_to_response
import json
import sys
from datetime import datetime
__author__ = 'zhouhaozhe'

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def upload_code(request):
    if request.method == 'POST':
        obj = request.FILES.get('file')
        project_name = request.POST.get('project_name')
        print project_name
        code_path = request.POST.get('code_path')
        print code_path
        # print(obj.name)
        code = ContentFile(obj.read())
        code_content = ""
        for chunk in code.chunks():
            code_content += chunk
        print code_content
        file.objects.create(code_content=code_content,
                            code_path = code_path,
                            project_name = project_name,
                            code_owner = request.session['user_name'],
                            update_time = datetime.now())
        return HttpResponseRedirect('/code/code_timeline')
    else:
        projects = user.objects.filter(user_name=request.session['user_name'])
        return render_to_response('pages/code/code_upload.html',{'projects':projects,'request':request,'username':request.session['user_name']})


def del_code(request):
    code_id = request.GET.get('id')
    code_owner = request.GET.get('code_owner')
    code = file.objects.filter(Q(id=code_id)&Q(code_owner=code_owner))
    if code.exists():
        code.delete()
    print "upload"


def code_timeline(request):
    if request.session['user_role'] == 'admin':
        code_file = file.objects.all().order_by("-update_time")
        print code_file
    else:
        user_filter = user.objects.filter(leader_name=request.session['user_name'])
        code_file = file.objects.filter(code_owner=request.session['user_name'])
        print code_file
        for user_one in user_filter:
            print user_one.user_name
            code_file = code_file | file.objects.filter(code_owner=user_one.user_name).order_by("-update_time")
            print len(code_file)
    return render_to_response('pages/code/code_timeline.html',{'code_file':code_file,'request':request,'username':request.session['user_name']})


def code_diff(request):
    now_code_id = request.GET.get("code_id")
    now_code_id = int(now_code_id)
    now_code = file.objects.filter(id=now_code_id)[0]
    print now_code.code_path
    before_code = file.objects.filter(Q(code_path = now_code.code_path)&Q(id__lt=now_code_id)&Q(code_owner=now_code.code_owner)).order_by("-update_time")
    if before_code.exists():
        return render_to_response('pages/code/code_diff.html',{"now_code":now_code,"before_code":before_code[0],"request":request,'username':request.session['user_name']})
    else:
        return render_to_response('pages/code/code_diff.html',{"now_code":now_code,"before_code":before_code,"request":request,'username':request.session['user_name']})

def use_old(request):
    code_id = request.POST.get("id",0)
    code_id = int(code_id)
    now_code = file.objects.filter(id=code_id)[0]
    print code_id
    print now_code.code_path
    before_code = file.objects.filter(Q(code_path = now_code.code_path)&Q(id__gt=code_id)&Q(code_owner=now_code.code_owner)).order_by("-update_time")
    if before_code.exists():
        before_code = before_code[0]
        file.objects.create(project_id = before_code.project_id,
                            project_name = before_code.project_name,
                            code_owner = request.session['user_name'],
                            code_path = before_code.code_path,
                            code_content = before_code.code_content,
                            update_time = datetime.now())
    else:
        file.objects.create(project_id = now_code.project_id,
                            project_name = now_code.project_name,
                            code_owner = request.session['user_name'],
                            code_path = now_code.code_path,
                            code_content = "",
                            update_time = datetime.now())

    return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")

def edit_new(request):
    if request.method == "POST":
        code_content = request.POST.get("code_content")
        code_id = request.POST.get("id")
        now_code = file.objects.filter(id=int(code_id))[0]
        print now_code.code_path
        file.objects.create(code_content=code_content,
                            code_path = now_code.code_path,
                            project_name = now_code.project_name,
                            code_owner = request.session['user_name'],
                            update_time = datetime.now())
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")


