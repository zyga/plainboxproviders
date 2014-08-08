# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providerbackend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='command',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='summary',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='providermetadata',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
