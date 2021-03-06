# Generated by Django 4.0.2 on 2022-04-23 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0013_alter_note_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelf', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShelfItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchased', models.DateTimeField(auto_now_add=True, null=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelfitems', to='base.note')),
                ('shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='base.shelf')),
            ],
        ),
    ]
