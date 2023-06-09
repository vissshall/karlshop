# Generated by Django 4.1.5 on 2023-03-29 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Maincategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subcategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
                ("baseprice", models.IntegerField()),
                ("discount", models.IntegerField(default=0)),
                ("finalprice", models.IntegerField()),
                ("stock", models.BooleanField(default=True)),
                ("description", models.TextField()),
                ("pic1", models.ImageField(upload_to="uploads/products")),
                (
                    "pic2",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="uploads/products",
                    ),
                ),
                (
                    "pic3",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="uploads/products",
                    ),
                ),
                (
                    "pic4",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="uploads/products",
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mainapp.brand"
                    ),
                ),
                (
                    "maincategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.maincategory",
                    ),
                ),
                (
                    "subcategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.subcategory",
                    ),
                ),
            ],
        ),
    ]
