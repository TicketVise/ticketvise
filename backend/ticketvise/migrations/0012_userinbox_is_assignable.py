# Generated by Django 3.1.3 on 2020-12-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0011_auto_20201204_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinbox',
            name='is_assignable',
            field=models.BooleanField(default=True),
        ),
    ]