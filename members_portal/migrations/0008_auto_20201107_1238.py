# Generated by Django 3.1.1 on 2020-11-07 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members_portal', '0007_addreview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addreview',
            old_name='Course',
            new_name='course',
        ),
    ]
