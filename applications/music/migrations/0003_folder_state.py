# Generated by Django 2.2.6 on 2023-05-10 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0002_auto_20230510_1156"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="state",
            field=models.CharField(default="none", max_length=32),
        ),
    ]
