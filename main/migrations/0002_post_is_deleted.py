# Generated by Django 4.0.6 on 2022-07-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='На удаление'),
        ),
    ]
