# Generated by Django 3.1.1 on 2020-11-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0014_discussion_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='comment_replied',
            field=models.IntegerField(null=True),
        ),
    ]
