# Generated by Django 4.0.3 on 2022-04-08 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='defined_check_in_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='defined_check_out_time',
            field=models.TimeField(),
        ),
    ]