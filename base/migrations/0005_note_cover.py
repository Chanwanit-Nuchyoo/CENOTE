# Generated by Django 4.0.2 on 2022-04-15 05:16

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_images_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='cover',
            field=models.ImageField(default=None, upload_to=base.models.cover_path),
            preserve_default=False,
        ),
    ]
