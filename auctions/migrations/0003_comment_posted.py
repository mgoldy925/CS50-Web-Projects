# Generated by Django 4.0.4 on 2022-05-30 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
