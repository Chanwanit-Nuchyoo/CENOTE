# Generated by Django 4.0.2 on 2022-04-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_account_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='like_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='view_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
