# Generated by Django 4.1 on 2022-11-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default_ykicap.jpg', null=True, upload_to='avatar'),
        ),
    ]
