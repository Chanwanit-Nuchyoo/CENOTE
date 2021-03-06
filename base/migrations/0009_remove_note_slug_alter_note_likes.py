# Generated by Django 4.0.2 on 2022-04-15 09:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_note_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='slug',
        ),
        migrations.AlterField(
            model_name='note',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='note_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
