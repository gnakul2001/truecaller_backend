# Generated by Django 4.2.4 on 2023-08-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contacts",
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
                ("contact_id", models.CharField(max_length=100)),
                ("user_id_imported_contacts", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                ("country_code", models.CharField(max_length=15)),
                ("phone_number", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SpamContacts",
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
                ("spam_id", models.CharField(max_length=100)),
                ("country_code", models.CharField(max_length=15)),
                ("phone_number", models.BigIntegerField()),
                ("spam_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("user_id", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                ("country_code", models.CharField(max_length=15)),
                ("phone_number", models.BigIntegerField()),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("password", models.CharField(max_length=150)),
                ("login_hash", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "login_hash_expires_at",
                    models.DateTimeField(blank=True, max_length=500, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserSpammedContacts",
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
                ("user_id", models.CharField(max_length=100)),
                ("spam_id", models.CharField(max_length=100)),
                ("spam_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
