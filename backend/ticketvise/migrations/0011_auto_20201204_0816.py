# Generated by Django 3.1.3 on 2020-12-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0010_auto_20201023_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notification_assigned_mail',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notification_comment_mail',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notification_mention_mail',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notification_new_ticket_mail',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notification_ticket_reminder_mail',
            field=models.BooleanField(default=True),
        ),
    ]
