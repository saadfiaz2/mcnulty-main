# Generated by Django 5.1.5 on 2025-02-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0013_alter_agent_phone_numbers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agent",
            name="phone_numbers",
            field=models.ManyToManyField(blank=True, to="myapp.phonenumber"),
        ),
    ]
