# Generated by Django 4.1.6 on 2023-02-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hello", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listofdownloads",
            name="file_name",
            field=models.CharField(default="", max_length=300),
        ),
    ]
