# Generated by Django 3.1.3 on 2020-11-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_f',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
