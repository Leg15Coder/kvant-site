# Generated by Django 3.2.9 on 2022-03-29 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0026_alter_profile_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, default='static\\img\\icon.ico', null=True, upload_to='images/icons/'),
        ),
        migrations.CreateModel(
            name='UnactiveProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16)),
                ('surname', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('patronymic', models.CharField(max_length=40)),
                ('birth_date', models.DateTimeField()),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='studentgroups',
            name='students',
            field=models.ManyToManyField(related_name='Ученики', to='blog.UnactiveProfile'),
        ),
    ]