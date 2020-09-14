from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='applicationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=40)),
                ('name', models.CharField(blank=True, max_length=40)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phoneNumber', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='applicationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('jobtype', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('AC', 'Accepted'), ('RJ', 'Rejected'), ('PR', 'Pending')], default='PR', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='educationExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('duration', models.CharField(max_length=20)),
                ('school', models.CharField(max_length=40)),
                ('major', models.CharField(max_length=40)),
                ('Username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='workExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=40)),
                ('years', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=150)),
                ('Username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=40)),
                ('Username', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=40)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phoneNumber', models.CharField(blank=True, max_length=15)),
                ('nickName', models.CharField(blank=True, max_length=20)),
                ('password', models.CharField(blank=True, max_length=40)),
                ('image', models.ImageField(default='default.png', upload_to='profile_image')),
                ('skills', models.ManyToManyField(to='users.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('banner', models.ImageField(default='boeing_logo.jpg', upload_to='company_logos')),
                ('name', models.CharField(blank=True, max_length=40, verbose_name='Company Name')),
                ('phoneNumber', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('company_description', models.CharField(blank=True, max_length=500, verbose_name="Company's Description")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
