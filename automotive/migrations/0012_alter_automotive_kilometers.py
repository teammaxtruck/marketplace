# Generated by Django 4.1.7 on 2023-03-29 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automotive', '0011_automotive_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automotive',
            name='kilometers',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
