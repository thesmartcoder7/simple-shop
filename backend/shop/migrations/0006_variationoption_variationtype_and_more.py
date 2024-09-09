# Generated by Django 5.1.1 on 2024-09-09 00:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productvariation_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_option_name', models.CharField(max_length=50)),
                ('price_change', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='VariationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='product_price',
            new_name='base_price',
        ),
        migrations.RemoveField(
            model_name='productvariation',
            name='variation_name',
        ),
        migrations.AddField(
            model_name='productvariation',
            name='variation_options',
            field=models.ManyToManyField(to='shop.variationoption'),
        ),
        migrations.AddField(
            model_name='variationoption',
            name='variation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='shop.variationtype'),
        ),
    ]
