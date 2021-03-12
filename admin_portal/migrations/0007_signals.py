# Generated by Django 3.1.1 on 2020-09-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0006_remove_discussion_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal_title', models.CharField(max_length=50)),
                ('signal_content', models.CharField(max_length=250)),
                ('signal_date', models.DateTimeField(auto_now=True)),
                ('members', models.CharField(max_length=50)),
            ],
        ),
    ]
