# Generated by Django 3.1.2 on 2020-10-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0007_auto_20201002_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='enable_create_new_ticket_by_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inbox',
            name='enable_reply_by_email',
            field=models.BooleanField(default=True),
        ),
    ]
