# Generated by Django 4.1.7 on 2023-04-30 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import proprety.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proprety', '0002_proprety_propretyimages_propretyfave_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(max_length=256, null=True, upload_to=proprety.models.upload_to_Prop),
        ),
        migrations.CreateModel(
            name='propretyads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.IntegerField(blank=True, default=0, editable=False)),
                ('type_locaction', models.IntegerField(blank=True, default=0, editable=False)),
                ('proprety', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads_proprety', to='proprety.proprety')),
                ('uid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pads_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
