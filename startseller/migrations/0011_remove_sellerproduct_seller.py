# Generated by Django 4.2.1 on 2023-09-10 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startseller', '0010_alter_sellerproduct_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerproduct',
            name='Seller',
        ),
    ]
