# Generated by Django 5.1.5 on 2025-01-16 14:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0005_remove_record_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="record",
            name="agent",
        ),
        migrations.DeleteModel(
            name="Agent",
        ),
    ]
