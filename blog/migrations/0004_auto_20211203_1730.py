# Generated by Django 3.2.9 on 2021-12-03 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20211203_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='name',
        ),
        migrations.AddField(
            model_name='messages',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
