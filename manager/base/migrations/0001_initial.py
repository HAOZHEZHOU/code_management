# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-02 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('user_pass', models.CharField(max_length=100)),
                ('role_name', models.CharField(max_length=10)),
                ('group_name', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='user_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='user_role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField()),
            ],
        ),
    ]