# Generated by Django 3.2.3 on 2021-08-28 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Uncategorised', 'Uncategorised'), ('Clothing', 'Clothing'), ('Home/Kitchen', 'Home/Kitchen'), ('Electronics', 'Electronics'), ('Books', 'Books'), ('Shoes', 'Shoes'), ('Sports', 'Sports')], default='Uncategorised', max_length=60),
        ),
    ]
