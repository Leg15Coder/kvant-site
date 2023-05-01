# Generated by Django 3.2.9 on 2021-12-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20211204_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminfield',
            old_name='adminF',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userfield',
            old_name='userF',
            new_name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='users_send',
            field=models.TextField(blank=True, null=True, verbose_name='Введитн через пробел участников чата'),
        ),
    ]