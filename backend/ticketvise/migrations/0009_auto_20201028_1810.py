# Generated by Django 3.1.1 on 2020-10-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0008_auto_20201027_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
