# Generated by Django 4.1.5 on 2023-04-30 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0008_contact"),
    ]

    operations = [
        migrations.AddField(
            model_name="buyer",
            name="otp",
            field=models.IntegerField(blank=True, default=1231212, null=True),
        ),
    ]
