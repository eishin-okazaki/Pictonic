# Generated by Django 4.2.15 on 2024-10-05 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_generatedimage_summary_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
