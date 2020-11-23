# Generated by Django 3.0.6 on 2020-11-22 15:30

import apply.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('apply', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickApply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to=apply.models.user_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
        ),
    ]