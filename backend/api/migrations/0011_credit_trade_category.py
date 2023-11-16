# Generated by Django 3.2.23 on 2023-11-06 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_migrate_compliance_report'),
    ]

    operations = [
        migrations.RunSQL("UPDATE credit_trade SET trade_category_id = null FROM credit_trade_type WHERE credit_trade.trade_category_id IS NOT NULL AND credit_trade_type.id = credit_trade.trade_category_id AND credit_trade_type.the_type NOT IN ('Buy', 'Sell');")
    ]