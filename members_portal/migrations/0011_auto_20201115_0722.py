# Generated by Django 3.1.1 on 2020-11-15 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members_portal', '0010_auto_20201115_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members_profile',
            name='phone_number',
            field=models.CharField(max_length=200),
        ),
    ]
