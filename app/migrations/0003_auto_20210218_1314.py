# Generated by Django 3.1.5 on 2021-02-18 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210215_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='locallity',
            new_name='locality',
        ),
    ]