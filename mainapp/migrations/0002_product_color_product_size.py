# Generated by Django 4.1.5 on 2023-03-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.CharField(default="Blue", max_length=20),
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.CharField(default="MD", max_length=20),
        ),
    ]
