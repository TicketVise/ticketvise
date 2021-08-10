# Generated by Django 3.1.5 on 2021-05-21 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0014_tickettitleevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_approved',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_pinned',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_public',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='pin_initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pin_initiator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='publish_request_created',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='publish_request_initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publish_request_initiator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_removed', models.DateTimeField(default=None, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relationship', to='ticketvise.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_relationship', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ticket')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='subscribed_tickets',
            field=models.ManyToManyField(related_name='users', through='ticketvise.UserTicket', to='ticketvise.Ticket'),
        ),
    ]
