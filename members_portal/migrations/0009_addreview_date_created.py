# Generated by Django 3.1.1 on 2020-11-08 19:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('members_portal', '0008_auto_20201107_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='addreview',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 11, 8, 19, 8, 14, 655908, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
