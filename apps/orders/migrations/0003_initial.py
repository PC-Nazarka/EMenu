# Generated by Django 3.2.16 on 2022-10-27 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0002_restaurantandorder_restaurant'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.client', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(related_name='orders', to='orders.Dish', verbose_name='Блюда'),
        ),
        migrations.AddField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.employee', verbose_name='Сотрудник'),
        ),
        migrations.AddField(
            model_name='dishimages',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='orders.dish', verbose_name='Блюдо'),
        ),
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='dish',
            name='reviews',
            field=models.ManyToManyField(related_name='dish', to='reviews.Review', verbose_name='Отзыв'),
        ),
    ]
