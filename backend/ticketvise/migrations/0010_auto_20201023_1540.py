# Generated by Django 3.1.2 on 2020-10-23 13:40

import uuid

from django.db import migrations, models


def set_initial_message_id(apps, schema_editor):
    for device in apps.get_model('ticketvise', 'Ticket').objects.all():
        device.reply_message_id = uuid.uuid4()
        device.comment_message_id = uuid.uuid4()
        device.save(update_fields=['reply_message_id', 'comment_message_id'])


class Migration(migrations.Migration):
    dependencies = [
        ('ticketvise', '0009_auto_20201028_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
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

        migrations.AddField(
            model_name='ticket',
            name='comment_message_id',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='reply_message_id',
            field=models.UUIDField(null=True),
        ),
        migrations.RunPython(set_initial_message_id),
        migrations.AlterField(
            model_name='ticket',
            name='comment_message_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reply_message_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
        )
    ]
