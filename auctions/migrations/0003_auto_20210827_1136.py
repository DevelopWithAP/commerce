# Generated by Django 3.2.3 on 2021-08-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.ManyToManyField(blank=True, to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='comment',
            field=models.ManyToManyField(blank=True, to='auctions.Comment'),
        ),
    ]