# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

class project(models.Model):
    project_id = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    project_intro = models.TextField()
    project_owner = models.CharField(max_length=200)
    project_creator = models.CharField(max_length=200)
    update_time = models.DateTimeField(default=datetime.datetime.now())


class file(models.Model):
    project_id = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    code_owner = models.CharField(max_length=200)
    code_path = models.TextField()
    code_content = models.TextField()
    update_time = models.DateTimeField()
# Create your models here.
