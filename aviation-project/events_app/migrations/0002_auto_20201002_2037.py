# Generated by Django 3.0.6 on 2020-10-02 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlisting',
            name='eventID',
        ),
        migrations.AddField(
            model_name='eventlisting',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.CompanyProfile'),
        ),
    ]
