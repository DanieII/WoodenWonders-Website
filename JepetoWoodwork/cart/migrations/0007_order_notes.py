# Generated by Django 4.2.3 on 2023-08-23 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_order_address_alter_order_apartment_building_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(default='', verbose_name='Бележки към поръчката (относно доставката или друго)'),
            preserve_default=False,
        ),
    ]
