# Generated by Django 4.2.7 on 2023-12-02 08:32

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
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_from', models.CharField(max_length=3)),
                ('currency_to', models.CharField(max_length=3)),
                ('amount_from', models.DecimalField(decimal_places=2, max_digits=15)),
                ('amount_to', models.DecimalField(decimal_places=2, max_digits=15)),
                ('exchange_rate', models.DecimalField(decimal_places=5, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]