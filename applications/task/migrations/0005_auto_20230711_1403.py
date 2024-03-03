# Generated by Django 2.2.6 on 2023-07-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0004_taskrecord_batch"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="name",
            new_name="full_path",
        ),
        migrations.AddField(
            model_name="task",
            name="filename",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="task",
            name="parent_path",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="task",
            name="state",
            field=models.CharField(default="wait", max_length=255),
        ),
    ]
