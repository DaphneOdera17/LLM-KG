# Generated by Django 5.0.7 on 2024-07-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kgllm", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="email",
            field=models.EmailField(default="", max_length=254),
        ),
    ]
