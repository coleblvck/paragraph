# Generated by Django 4.1.8 on 2023-08-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediashare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedmedia',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='shared_media/'),
        ),
    ]
