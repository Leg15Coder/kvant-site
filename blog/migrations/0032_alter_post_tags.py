# Generated by Django 3.2.9 on 2022-05-13 16:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20220513_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=30, null=True), blank=True, null=True, size=10),
        ),
    ]
