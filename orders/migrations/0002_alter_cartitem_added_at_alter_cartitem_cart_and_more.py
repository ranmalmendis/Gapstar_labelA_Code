# Generated by Django 4.0.3 on 2024-02-22 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The datetime when the item was added to the cart.'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(help_text='The shopping cart to which this item belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.shoppingcart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(help_text='The specific product this cart item represents.', on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, help_text='The quantity of the product.'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.shoppingcart', verbose_name='Linked shopping cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='Scheduled delivery date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(verbose_name='Scheduled delivery time'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Order timestamp'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Ordering user'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when the shopping cart was created.', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.OneToOneField(help_text='The user this shopping cart belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]