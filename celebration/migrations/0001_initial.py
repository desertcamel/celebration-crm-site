# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(null=True)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='files/%Y')),
            ],
        ),
        migrations.CreateModel(
            name='Occassion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occassion_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_Date', models.DateField(blank=True, null=True)),
                ('Order_No', models.IntegerField(blank=True, null=True)),
                ('Total_Amount', models.FloatField(blank=True, null=True)),
                ('Delivery_Time', models.CharField(blank=True, max_length=100)),
                ('Delivery_Mode', models.CharField(blank=True, max_length=100)),
                ('Branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='celebration.Branch')),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='celebration.Company')),
                ('Customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='celebration.Customer')),
                ('Occassion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='celebration.Occassion')),
            ],
        ),
    ]
