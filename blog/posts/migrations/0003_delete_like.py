# Generated by Django 5.0.4 on 2024-04-22 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]