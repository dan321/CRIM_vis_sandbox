# Generated by Django 2.2.2 on 2019-06-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualisations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='piece_id',
            field=models.CharField(default=-1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='piece',
            name='title',
            field=models.CharField(default=-1, max_length=255),
            preserve_default=False,
        ),
    ]
