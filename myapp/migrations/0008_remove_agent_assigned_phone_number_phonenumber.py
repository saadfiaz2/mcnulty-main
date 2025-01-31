# Generated by Django 5.1.5 on 2025-01-31 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0007_agent_record_agent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="assigned_phone_number",
        ),
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(max_length=15, unique=True)),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phone_numbers",
                        to="myapp.agent",
                    ),
                ),
            ],
        ),
    ]
