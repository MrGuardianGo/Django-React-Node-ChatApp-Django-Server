# Generated by Django 4.1 on 2022-08-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default_ykicap.jpg', upload_to='', verbose_name='avatar'),
        ),
    ]
