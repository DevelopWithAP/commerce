# Generated by Django 3.2.3 on 2021-08-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210827_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('0', 'Uncategorised'), ('1', 'Clothing'), ('2', 'Home/Kitchen'), ('3', 'Electronics'), ('4', 'Books'), ('5', 'Shoes'), ('6', 'Sports')], default='0', max_length=60),
        ),
    ]
