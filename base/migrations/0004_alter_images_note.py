# Generated by Django 4.0.2 on 2022-04-14 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_note_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='note',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.note'),
        ),
    ]
