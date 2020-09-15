# Generated by Django 3.1 on 2020-09-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0005_auto_20200911_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('PNDG', 'Pending'), ('ASGD', 'Assigned'), ('ANSD', 'Awaiting response'), ('CLSD', 'Closed')], default='PNDG', max_length=8),
        ),
        migrations.AlterField(
            model_name='ticketstatusevent',
            name='new_status',
            field=models.CharField(choices=[('PNDG', 'Pending'), ('ASGD', 'Assigned'), ('ANSD', 'Awaiting response'), ('CLSD', 'Closed')], max_length=8),
        ),
        migrations.AlterField(
            model_name='ticketstatusevent',
            name='old_status',
            field=models.CharField(choices=[('PNDG', 'Pending'), ('ASGD', 'Assigned'), ('ANSD', 'Awaiting response'), ('CLSD', 'Closed')], max_length=8, null=True),
        ),
    ]