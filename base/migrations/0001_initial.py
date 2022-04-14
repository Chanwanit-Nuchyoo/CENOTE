# Generated by Django 4.0.2 on 2022-04-14 07:03

import base.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('info', models.TextField(max_length=100)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('pdf_file', models.FileField(upload_to=base.models.image_path)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=600, null=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=base.models.image_path)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.note')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.note')),
            ],
        ),
    ]