# Generated by Django 3.2.9 on 2022-05-20 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
    ]
