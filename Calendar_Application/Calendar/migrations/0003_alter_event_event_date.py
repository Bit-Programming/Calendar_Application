# Generated by Django 5.1.1 on 2024-09-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(verbose_name='Event Date'),
        ),
    ]
