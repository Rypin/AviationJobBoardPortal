# Generated by Django 3.0.6 on 2020-09-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventID', models.IntegerField(unique=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='company_logos')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('posted', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
            ],
        ),
    ]
