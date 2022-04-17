# Generated by Django 4.0.2 on 2022-04-15 08:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_alter_note_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='likes',
            field=models.ManyToManyField(related_name='note_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
