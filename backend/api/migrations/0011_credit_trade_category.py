# Generated by Django 3.2.23 on 2023-11-06 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_migrate_compliance_report'),
    ]

    operations = [
        migrations.RunSQL("UPDATE credit_trade SET trade_category_id = NULL WHERE type_id != 1 AND type_id != 2")
    ]
