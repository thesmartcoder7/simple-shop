# Generated by Django 5.1.1 on 2024-09-09 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_variationoption_variationtype_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variationoption',
            old_name='v_option_name',
            new_name='option_name',
        ),
    ]
