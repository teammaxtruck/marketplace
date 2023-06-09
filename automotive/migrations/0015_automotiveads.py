# Generated by Django 4.1.7 on 2023-04-16 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('automotive', '0014_alter_automotive_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='automotiveads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.IntegerField(blank=True, default=0, editable=False)),
                ('type_locaction', models.IntegerField(blank=True, default=0, editable=False)),
                ('automotive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads_automotive', to='automotive.automotive')),
                ('uid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ads_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
