# Generated by Django 3.1.1 on 2020-11-13 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0016_auto_20201107_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
    ]