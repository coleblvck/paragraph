# Generated by Django 4.2.2 on 2023-06-26 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0002_alter_textmessage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmessage',
            name='body',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
    ]
