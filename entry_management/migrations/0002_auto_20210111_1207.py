# Generated by Django 3.1.3 on 2021-01-11 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry_info',
            old_name='author_entry',
            new_name='author',
        ),
    ]
