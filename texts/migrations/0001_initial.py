# Generated by Django 4.2.2 on 2023-06-13 03:42

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
            name='TextMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, max_length=1000, null=True)),
                ('edittime', models.DateTimeField(auto_now=True, verbose_name='edit time')),
                ('seen', models.BooleanField(default=False)),
                ('textreceiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textreceiver', to=settings.AUTH_USER_MODEL)),
                ('textsender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textsender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-edittime',),
            },
        ),
    ]
