# Generated by Django 3.1.1 on 2020-10-27 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ticketvise.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0007_auto_20201021_1745'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', ticketvise.models.user.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='inbox',
            name='scheduling_algorithm',
            field=models.CharField(choices=[('round-robin', 'Round Robin'), ('least-assigned-first', 'Least Assigned First'), ('sections', 'Workgroup'), ('fixed', 'Fixed')], default='least-assigned-first', max_length=255),
        ),
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
