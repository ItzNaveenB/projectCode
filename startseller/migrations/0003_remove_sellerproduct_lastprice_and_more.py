# Generated by Django 4.2.1 on 2023-09-08 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startseller', '0002_alter_businessinfo_user_alter_productinfo_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerproduct',
            name='LastPrice',
        ),
        migrations.RemoveField(
            model_name='sellerproduct',
            name='LastPriceDate',
        ),
        migrations.RemoveField(
            model_name='sellerproduct',
            name='seller',
        ),
    ]