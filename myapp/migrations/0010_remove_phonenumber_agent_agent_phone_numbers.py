# Generated by Django 5.1.5 on 2025-01-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0009_alter_phonenumber_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="phonenumber",
            name="agent",
        ),
        migrations.AddField(
            model_name="agent",
            name="phone_numbers",
            field=models.ManyToManyField(to="myapp.phonenumber"),
        ),
    ]
