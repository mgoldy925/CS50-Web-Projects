# Generated by Django 4.0.4 on 2022-07-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.CharField(default='error/Error with profile URL.', max_length=100),
        ),
    ]