# Generated by Django 3.0.6 on 2020-09-08 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0002_auto_20200906_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PR', 'Pending Review'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('SB', 'Submitted')], default='SB', max_length=2)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apply.Application')),
            ],
        ),
    ]