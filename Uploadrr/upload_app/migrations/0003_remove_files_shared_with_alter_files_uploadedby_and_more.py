# Generated by Django 5.0 on 2023-12-07 12:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_app', '0002_alter_files_shared_with'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='shared_with',
        ),
        migrations.AlterField(
            model_name='files',
            name='uploadedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploader_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='files',
            name='shared_with',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to=settings.AUTH_USER_MODEL),
        ),
    ]