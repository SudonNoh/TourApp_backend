# Generated by Django 4.0.6 on 2022-07-22 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
