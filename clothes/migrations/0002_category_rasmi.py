# Generated by Django 5.1.4 on 2024-12-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='rasmi',
            field=models.URLField(default='default_value', max_length=255),
        ),
    ]
