# Generated by Django 4.1.7 on 2023-04-09 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automotive', '0013_alter_subcatgoriess_options_brands_is_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automotive',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='automotive',
            name='is_publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='automotive',
            name='view',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
