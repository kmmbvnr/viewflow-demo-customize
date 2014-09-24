# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm
from django.conf import settings
import viewflow.token
import viewflow.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShipmentProcess',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('flow_cls', viewflow.fields.FlowReferenceField(max_length=250)),
                ('status', django_fsm.FSMField(choices=[('NEW', 'New'), ('STR', 'Stated'), ('FNS', 'Finished'), ('ERR', 'Error')], max_length=3, default='NEW')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('address', models.TextField()),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShipmentTask',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('flow_task', viewflow.fields.TaskReferenceField(max_length=150)),
                ('flow_task_type', models.CharField(max_length=50)),
                ('status', django_fsm.FSMField(choices=[('NEW', 'New'), ('ASN', 'Assigned'), ('PRP', 'Prepared for execution'), ('STR', 'Stated'), ('FNS', 'Finished'), ('CNC', 'Cancelled'), ('ERR', 'Error')], db_index=True, max_length=3, default='NEW')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('token', viewflow.fields.TokenField(max_length=150, default=viewflow.token.Token('start'))),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('previous', models.ManyToManyField(to='parcel.ShipmentTask', related_name='previous_rel_+')),
                ('process', models.ForeignKey(to='parcel.ShipmentProcess')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shipmentitem',
            name='shipment',
            field=models.ForeignKey(to='parcel.ShipmentProcess'),
            preserve_default=True,
        ),
    ]
