# Generated by Django 3.1.5 on 2021-03-05 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0014_tickettitleevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_public',
            field=models.BooleanField(default=False),
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
    ]
