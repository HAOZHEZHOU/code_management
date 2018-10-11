from __future__ import unicode_literals
from django.template import loader,Context
from django.http import HttpResponse
from manager.base.models import user,user_role,user_group
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from datetime import datetime
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
import hashlib
__author__ = 'zhouhaozhe'

class LocalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(LocalEncoder, self).default(obj)

def logout(request):
    return render_to_response('login.html',{'request':request},RequestContext(request))

def login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_pass = request.POST['user_pass']
        user_pass = hashlib.md5(user_pass.encode('utf-8')).hexdigest()
        user_one = user.objects.filter(user_name=user_name,user_pass=user_pass)
        print user_one
        if user_one.exists():
            print 'dengluchengong'
            print request.session
            role_name = user_one[0].role_name
            print role_name
            request.session['session_name'] =user_name
            request.session['user_role']=role_name
            request.session['user_name'] = user_name
            request.session['leader_name'] = user_one[0].leader_name
            request.session['project_name'] = user_one[0].project_name
            return HttpResponseRedirect('/base/message')
        else:
            return HttpResponseRedirect('/base/login/')
    else:
        return render_to_response('login.html',{'request':request},RequestContext(request))

def add_user(request):
    print 'djajsdadasdsadsssssssssssssssssssssssssssss'
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_pass = request.POST['user_pass']
        real_name = request.POST['real_name']
        user_pass = hashlib.md5(user_pass.encode('utf-8')).hexdigest()
        role_id = request.POST['user_role']
        role_id = int(role_id)
        user_leader = request.POST.get('user_leader',0)
        print role_id
        role_name = user_role.objects.filter(id = role_id)
        if role_name.exists():
            role_name = role_name[0].role_name
        else:
            role_name = 'user'
        leader_name = user_leader
        user_one = user.objects.filter(user_name=user_name)
        if user_one.exists():
            user_one.update(real_name=real_name,user_pass=user_pass,role_name = role_name,leader_name=leader_name)
        else:
            user.objects.create(user_name=user_name,real_name=real_name,user_pass=user_pass,role_name = role_name,leader_name=leader_name)
        role = user_role.objects.all()
        group = user_group.objects.all()
        return render_to_response('pages/base/user_list.html',{'role':role,'group':group,'request':request,'username':request.session['user_name']})
    else:
        role = user_role.objects.all()
        group = user_group.objects.all()
        ajax = request.GET.get('ajax',0)
        if ajax == 1:
            return
        return render_to_response('pages/base/user_list.html',{'role':role,'group':group,'request':request,'username':request.session['user_name']})


def user_list(request):
    if request.method == 'POST':
        start = request.POST['iDisplayStart']
        begin = int(start)
        length = request.POST['iDisplayLength']
        end = int(length) + int(start)
        users = user.objects.all()
        aData = users[begin:end]
        aData = json.loads(serializers.serialize("json", aData, cls=LocalEncoder))
        response_data = {"data": aData, "recordsTotal": len(users), "recordsFiltered": len(users)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        role = user_role.objects.all()
        user_list = user.objects.all()
        return render_to_response('pages/base/user_list.html',{'role':role,'user':user_list,'request':request,'username':request.session['user_name']})


def remove_user(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user.objects.filter(id = user_id).delete()

def remove_group(request):
    if request.method == 'POST':
        group_id = request.POST['group_id']
        user_group.objects.filter(id = group_id).delete()

def add_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        user_group.objects.create(group_name=group_name)
        return render_to_response('pages/base/group_list.html',{'username':request.session['user_name']})
    else:
        return render_to_response('pages/base/group_list.html',{'username':request.session['user_name']})


def group_list(request):
    if request.method == 'POST':
        start = request.POST['iDisplayStart']
        begin = int(start)
        length = request.POST['iDisplayLength']
        end = int(length) + int(start)
        groups = user_group.objects.all()
        aData = groups[begin:end]
        aData = json.loads(serializers.serialize("json", aData, cls=LocalEncoder))
        response_data = {"data": aData, "recordsTotal": len(groups), "recordsFiltered": len(groups)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render_to_response('pages/base/group_list.html',{'request':request,'username':request.session['user_name']})