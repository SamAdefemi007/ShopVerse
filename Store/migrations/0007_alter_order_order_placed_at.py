# Generated by Django 4.0.4 on 2022-05-10 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_placed_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
