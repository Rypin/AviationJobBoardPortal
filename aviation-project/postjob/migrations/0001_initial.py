from django.db import migrations, models
import django.db.models.deletion
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Jobform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('postdate', models.DateField()),
                ('posttime', models.TimeField()),
                ('deadlinedate', models.DateField()),
                ('deadlinetime', models.TimeField()),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('geolocation', django_google_maps.fields.GeoLocationField(max_length=100)),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('US_author_required', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CompanyProfile')),
                ('jobtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postjob.Jobtype')),
            ],
        ),
    ]
