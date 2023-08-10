# Generated by Django 4.1.8 on 2023-08-07 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('paragraphkey', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('body', models.TextField(blank=True, default='', max_length=1000)),
                ('edittime', models.DateTimeField(auto_now=True, verbose_name='edit time')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-edittime',),
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('notekey', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('body', models.TextField(blank=True, default='', max_length=1000)),
                ('edittime', models.DateTimeField(auto_now=True, verbose_name='edit time')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-edittime',),
            },
        ),
    ]