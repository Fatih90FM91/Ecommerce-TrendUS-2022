# Generated by Django 3.2.14 on 2022-07-22 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='date_added',
        ),
    ]
