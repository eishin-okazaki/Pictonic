# Generated by Django 4.2.15 on 2024-10-03 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_generatedimage_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedimage',
            name='summary_text',
            field=models.TextField(null=True),
        ),
    ]