# Generated by Django 5.1.1 on 2024-09-09 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_rename_v_option_name_variationoption_option_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variationtype',
            old_name='variation_type_name',
            new_name='variation_name',
        ),
    ]
