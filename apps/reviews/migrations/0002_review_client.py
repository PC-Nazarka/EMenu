# Generated by Django 3.2.14 on 2022-11-09 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='users.client', verbose_name='Клиент'),
        ),
    ]
