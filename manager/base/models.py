# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

class user(models.Model):
    user_name = models.CharField(max_length=50)
    user_pass = models.CharField(max_length=100)
    role_name = models.CharField(max_length=100)
    leader_name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    real_name = models.CharField(max_length=200,default='')
    update_time = models.DateTimeField(default=datetime.datetime.now())

class user_group(models.Model):
    group_name = models.CharField(max_length=200)
    update_time = models.DateTimeField(default=datetime.datetime.now())

class user_role(models.Model):
    role_name = models.CharField(max_length=200)
    update_time = models.DateTimeField(default=datetime.datetime.now())

class user_message(models.Model):
    from_user = models.CharField(max_length=200)
    to_user = models.CharField(max_length=200)
    message_content = models.TextField()
    create_time = models.DateTimeField(default=datetime.datetime.now())
    is_read = models.CharField(max_length=200,default=0)


class audit_log(models.Model):
    user_name = models.CharField(max_length=32)
    role_name = models.CharField(max_length=20)
    ip = models.CharField(max_length=32)
    uri = models.CharField(max_length=64)
    method = models.CharField(max_length=30)
    status_code = models.CharField(max_length=30)
    params = models.TextField()
    description = models.CharField(max_length=256)
    insert_time = models.DateTimeField()
    handler = models.CharField(max_length=50)
    handle_time = models.DateTimeField()
    remark = models.CharField(max_length=255)