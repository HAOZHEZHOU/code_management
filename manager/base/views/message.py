from __future__ import unicode_literals
from django.template import loader,Context
from django.http import HttpResponse
from manager.base.models import user,user_role,user_group,user_message
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from datetime import datetime
from django.db.models import Q
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
import hashlib
class LocalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(LocalEncoder, self).default(obj)
__author__ = 'zhouhaozhe'

def message_list(request):
    if request.session['user_role'] == 'admin':
        users = user.objects.all()
        all_message = user_message.objects.filter(Q(from_user=request.session['user_name'])| Q(to_user = request.session['user_name']))
        unread_message = user_message.objects.filter(Q(to_user=request.session['user_name'])&Q(is_read=0))

    else:
        users = user.objects.filter(leader_name = request.session['user_name'])
        leader_one = user.objects.filter(user_name = request.session['user_name'])
        if leader_one.exists():
            users = leader_one | users | user.objects.filter(user_name = leader_one[0].leader_name)
        all_message = user_message.objects.filter(Q(from_user=request.session['user_name'])| Q(to_user = request.session['user_name']))
        unread_message = user_message.objects.filter(Q(to_user=request.session['user_name'])&Q(is_read=0))
    users = json.loads(serializers.serialize("json", users, cls=LocalEncoder))
    return HttpResponse(json.dumps(users), content_type="application/json")


def message(request):
    return render_to_response('pages/base/user_chat.html',{"request":request,'username':request.session['user_name']})

def add_message(request):
    if request.method == 'POST':
        to_user = request.POST.get('user_name')
        from_user = request.session['user_name']
        message_content = request.POST.get('message_content')
        user_message.objects.create(from_user = request.session['user_name'],
                            to_user = to_user,
                            message_content = message_content,
                            is_read=0)
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")

def read_message(request):
    user_name = request.POST.get('from_user')
    messages = user_message.objects.filter((Q(from_user=user_name)&Q(to_user=request.session['user_name']))|(
        Q(from_user=request.session['user_name'])&Q(to_user=user_name)
                                                                                                            )).order_by("create_time")
    messages.update(is_read=1)
    messages = json.loads(serializers.serialize("json", messages, cls=LocalEncoder))
    return HttpResponse(json.dumps(messages), content_type="application/json")

def new_message_count(request):
    unread_message = user_message.objects.filter(Q(to_user=request.session['user_name'])&Q(is_read=0))
    return HttpResponse(json.dumps({"count":len(unread_message)}), content_type="application/json")

def send_message(request):
    if request.method == 'POST':
        to_user = request.POST.get('to_user')
        message_content = request.POST.get('message_content')
        if to_user == 'all':
            users = user.objects.all()
            for user_one in users:
                user_message.objects.create(to_user = user_one.user_name,
                                    from_user = request.session['user_name'],
                                    message_content = message_content,
                                    is_read = 0)
        else:
            user_message.objects.create(to_user = to_user,
                                from_user = request.session['user_name'],
                                message_content = message_content,
                                is_read = 0)
        return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")
