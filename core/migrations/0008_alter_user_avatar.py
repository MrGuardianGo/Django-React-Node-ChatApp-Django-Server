# Generated by Django 4.1 on 2022-08-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, default='https://res.cloudinary.com/cloudofmrguardian/image/upload/v1661687800/default_ykicap.jpg', max_length=10000, null=True),
        ),
    ]