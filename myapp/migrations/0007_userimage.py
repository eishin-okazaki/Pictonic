# Generated by Django 4.2.15 on 2024-09-06 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_postimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_path', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(1, 'オリジナル画像'), (2, '生成画像')], default=1)),
                ('status', models.IntegerField(choices=[(1, 'アクティブ'), (2, '非アクティブ')], default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
