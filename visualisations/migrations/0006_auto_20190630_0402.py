# Generated by Django 2.2.2 on 2019-06-30 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualisations', '0005_piece_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='piece',
            name='composer',
        ),
        migrations.RemoveField(
            model_name='piece',
            name='date',
        ),
        migrations.RemoveField(
            model_name='piece',
            name='genre',
        ),
    ]
