# Generated by Django 4.1.7 on 2023-04-30 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jobs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usersapp', '0006_user_bg_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(max_length=256, null=True, upload_to=jobs.models.upload_to_job)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Economicactivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Eductation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='jobs.category')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=512, null=True)),
                ('lastname', models.CharField(blank=True, max_length=512, null=True)),
                ('sex', models.BooleanField(default=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to=jobs.models.upload_to_cv)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('longitude', models.CharField(blank=True, max_length=512, null=True)),
                ('latitude', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.country')),
                ('eductation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.eductation')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.state')),
                ('uid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('license_file', models.FileField(blank=True, null=True, upload_to=jobs.models.upload_to_license_files)),
                ('logo', models.ImageField(blank=True, max_length=255, null=True, upload_to=jobs.models.upload_to_logos)),
                ('cover_image', models.ImageField(blank=True, max_length=255, null=True, upload_to=jobs.models.upload_to_logos)),
                ('website', models.CharField(blank=True, max_length=512, null=True)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('longitude', models.CharField(blank=True, max_length=512, null=True)),
                ('latitude', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.country')),
                ('economicactivity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.economicactivity')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usersapp.state')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.subcategory')),
                ('uid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
