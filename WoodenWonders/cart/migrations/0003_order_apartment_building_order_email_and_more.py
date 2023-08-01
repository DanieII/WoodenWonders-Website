# Generated by Django 4.2.3 on 2023-08-01 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_user_orderproduct_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='apartment_building',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone_numbe',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
