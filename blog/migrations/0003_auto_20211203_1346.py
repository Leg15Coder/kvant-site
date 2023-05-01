# Generated by Django 3.2.9 on 2021-12-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_file_f'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='file_f',
        ),
    ]
