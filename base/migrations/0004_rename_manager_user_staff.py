# Generated by Django 4.0.3 on 2022-04-02 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='manager',
            new_name='staff',
        ),
    ]
