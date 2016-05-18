# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('applicant', models.CharField(max_length=300)),
                ('facilityType', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('permit', models.CharField(max_length=100)),
                ('foodItems', models.CharField(max_length=500)),
                ('lat', models.DecimalField(max_digits=20, decimal_places=13)),
                ('lon', models.DecimalField(max_digits=20, decimal_places=13)),
                ('daysHours', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
    ]
