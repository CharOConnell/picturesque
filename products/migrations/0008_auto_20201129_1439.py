# Generated by Django 3.1.3 on 2020-11-29 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_category_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='image',
            new_name='category_image',
        ),
    ]