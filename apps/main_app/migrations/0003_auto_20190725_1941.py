# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-25 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.FileField(upload_to='products/photos/'),
        ),
    ]
