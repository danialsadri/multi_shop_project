# Generated by Django 4.2.6 on 2023-10-24 08:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_contactus_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 24, 8, 35, 28, 94392, tzinfo=datetime.timezone.utc)),
        ),
    ]
