# Generated by Django 3.2.6 on 2021-09-05 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0018_alter_ticketattachment_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inbox',
            old_name='image',
            new_name='image_old',
        ),
        
    ]
