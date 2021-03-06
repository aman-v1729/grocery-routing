# Generated by Django 3.0.4 on 2020-04-06 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0003_auto_20200406_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='warehouse_latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='warehouse_longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]
