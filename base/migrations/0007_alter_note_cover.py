# Generated by Django 4.0.2 on 2022-04-15 05:26

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_note_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='cover',
            field=models.ImageField(blank=True, default=base.models.default_cover, null=True, upload_to=base.models.cover_path),
        ),
    ]
