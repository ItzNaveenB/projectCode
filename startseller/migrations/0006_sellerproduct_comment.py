# Generated by Django 4.2.1 on 2023-09-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startseller', '0005_alter_sellerreview_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerproduct',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
    ]
