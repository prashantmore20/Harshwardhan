# Generated by Django 3.1.6 on 2021-03-28 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='discription',
            field=models.TextField(default='null', max_length=500),
            preserve_default=False,
        ),
    ]
