# Generated by Django 4.0.3 on 2022-04-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='infoappeal',
            name='answer_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inforequest',
            name='answer_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]