# Generated by Django 5.1.1 on 2024-09-22 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('event_start_time', models.TimeField(verbose_name='Event Start Time')),
                ('event_end_time', models.TimeField(verbose_name='Event End Time')),
                ('event_name', models.CharField(max_length=200)),
                ('event_description', models.TextField()),
            ],
        ),
    ]
