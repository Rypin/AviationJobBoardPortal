# Generated by Django 3.0.6 on 2020-10-02 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0002_auto_20201002_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlisting',
            name='image',
        ),
    ]