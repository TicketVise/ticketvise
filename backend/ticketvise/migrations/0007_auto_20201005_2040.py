# Generated by Django 3.1.2 on 2020-10-05 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0006_auto_20200913_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='shared_with',
        ),
        migrations.AddField(
            model_name='ticketshareduser',
            name='sharer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shared_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticketshareduser',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to='ticketvise.ticket'),
        ),
        migrations.AlterField(
            model_name='ticketshareduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with_me', to=settings.AUTH_USER_MODEL),
        ),
    ]
