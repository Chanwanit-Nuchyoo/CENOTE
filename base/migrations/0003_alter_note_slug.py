# Generated by Django 4.0.2 on 2022-04-14 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_note_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, max_length=600, null=True, unique=True),
        ),
    ]
