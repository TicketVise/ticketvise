# Generated by Django 3.1 on 2020-08-24 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inbox',
            old_name='show_assignee',
            new_name='show_assignee_to_guest',
        ),
    ]
