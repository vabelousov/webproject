# Generated by Django 3.0.5 on 2020-04-21 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_profile_email_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='media/images/users', verbose_name='Avatar image'),
        ),
    ]
