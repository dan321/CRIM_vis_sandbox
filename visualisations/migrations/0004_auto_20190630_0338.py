# Generated by Django 2.2.2 on 2019-06-30 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualisations', '0003_auto_20190623_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='composer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='piece',
            name='date',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
