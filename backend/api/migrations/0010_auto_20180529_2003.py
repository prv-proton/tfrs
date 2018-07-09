# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 20:03
from __future__ import unicode_literals

import api.validators
from decimal import Decimal
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_signingauthorityassertion_signingauthorityconfirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credittrade',
            name='fair_market_value_per_credit',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=999, null=True, validators=[api.validators.CreditTradeFairMarketValueValidator]),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]