# Generated by Django 4.1 on 2022-11-08 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_groupmessage_roomid_alter_user_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmessage',
            name='roomID',
            field=models.IntegerField(),
        ),
    ]
