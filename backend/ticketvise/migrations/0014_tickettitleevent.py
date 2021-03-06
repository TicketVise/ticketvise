# Generated by Django 3.1.5 on 2021-02-24 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketvise', '0013_user_give_introduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketTitleEvent',
            fields=[
                ('ticketevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ticketvise.ticketevent')),
                ('old_title', models.CharField(max_length=100)),
                ('new_title', models.CharField(max_length=100)),
            ],
            bases=('ticketvise.ticketevent',),
        ),
    ]
