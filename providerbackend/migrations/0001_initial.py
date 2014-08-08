# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderManagePy',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('path', models.CharField(help_text='path to manage.py within the repository', max_length=1024)),
                ('problem', models.TextField(null=True)),
            ],
            options={
                'verbose_name_plural': 'provider manage.py files',
                'verbose_name': 'provider manage.py file',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderMetaData',
            fields=[
                ('manage_py', models.OneToOneField(to='providerbackend.ProviderManagePy', serialize=False, primary_key=True)),
                ('pb_id', models.CharField(max_length=1024)),
                ('namespace', models.CharField(editable=False, max_length=1024)),
                ('version', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('gettext_domain', models.CharField(max_length=1024, null=True)),
            ],
            options={
                'verbose_name_plural': 'provider metadata objects',
                'verbose_name': 'provider metadata object',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('url', models.CharField(help_text="vcs-specific URL or path for 'local' vcs", max_length=4096)),
                ('vcs', models.CharField(max_length=16, choices=[('bzr', 'Bazaar'), ('git', 'Git'), ('local', 'Local Directory')])),
                ('updated_on', models.DateTimeField(null=True, auto_now=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('probed_on', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': 'repositories',
                'verbose_name': 'repository',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='providermanagepy',
            name='repo',
            field=models.ForeignKey(to='providerbackend.Repository', verbose_name='related repository'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('pb_id', models.CharField(max_length=1024)),
                ('unit', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('unit', models.OneToOneField(to='providerbackend.Unit', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=1024, null=True)),
                ('summary', models.CharField(max_length=1024, null=True)),
                ('plugin', models.CharField(max_length=1024, null=True)),
                ('command', models.CharField(max_length=1024, null=True)),
                ('description', models.TextField(null=True)),
                ('user', models.CharField(max_length=1024, null=True)),
                ('environ', models.TextField(null=True)),
                ('estimated_duration', models.CharField(max_length=1024, null=True)),
                ('depends', models.TextField(null=True)),
                ('requires', models.TextField(null=True)),
                ('shell', models.CharField(max_length=1024, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='unit',
            name='provider_metadata',
            field=models.ForeignKey(to='providerbackend.ProviderMetaData', verbose_name='related provider'),
            preserve_default=True,
        ),
    ]
