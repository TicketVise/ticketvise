# Generated by Django 3.1.1 on 2020-10-22 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0006_auto_20200913_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='InboxSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('inbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='ticketvise.inbox')),
            ],
            options={
                'unique_together': {('code', 'inbox')},
            },
        ),
        migrations.CreateModel(
            name='InboxUserSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_users', to='ticketvise.inboxsection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_sections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'section')},
            },
        ),
    ]
