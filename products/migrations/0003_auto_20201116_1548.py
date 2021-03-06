# Generated by Django 3.1.3 on 2020-11-16 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201105_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(choices=[('xs', 7.99), ('s', 10.99), ('m', 12.99), ('l', 15.99), ('xl', 18.99), ('xxl', 20.99)], decimal_places=2, default='xs', max_digits=6),
        ),
    ]
