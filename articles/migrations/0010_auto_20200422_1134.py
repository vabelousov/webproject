# Generated by Django 3.0.5 on 2020-04-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20200421_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='article', help_text='Choose type of the article from the drop-list', max_length=20),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', help_text='Choose status of the article from the drop-list', max_length=10),
        ),
    ]
