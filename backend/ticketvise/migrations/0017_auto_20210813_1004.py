# Generated by Django 3.2.6 on 2021-08-13 08:04

from django.db import migrations, models
import ticketvise.models.ticket


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0016_email_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='image',
            field=models.URLField(default='/img/default-inbox.png', max_length=255),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='inbound_email_protocol',
            field=models.CharField(choices=[('POP3', 'Pop3'), ('IMAP', 'Imap')], default='IMAP', max_length=4),
        ),
        migrations.AlterField(
            model_name='ticketattachment',
            name='file',
            field=models.FileField(max_length=1000, upload_to=ticketvise.models.ticket.ticket_directory_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(default='/img/default-avatar.png'),
        ),
    ]