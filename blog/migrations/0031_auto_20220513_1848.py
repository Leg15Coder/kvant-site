# Generated by Django 3.2.9 on 2022-05-13 15:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_alter_reaction_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=30), blank=True, null=True, size=10),
        ),
        migrations.AlterField(
            model_name='unactiveprofile',
            name='code',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]