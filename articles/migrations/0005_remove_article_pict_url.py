# Generated by Django 3.0.5 on 2020-04-18 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20200418_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='pict_url',
        ),
    ]
