# Generated by Django 4.1.3 on 2022-11-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_order_ref_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cash',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='plastic',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.IntegerField(),
        ),
    ]
