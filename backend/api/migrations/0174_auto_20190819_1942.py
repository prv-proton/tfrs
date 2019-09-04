# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-19 19:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0173_auto_20190819_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compliancereport',
            name='status_django_pacifier',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='compliance_report', to='api.ComplianceReportWorkflowState'),
        ),
    ]