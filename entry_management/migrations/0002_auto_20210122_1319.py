# Generated by Django 3.1.3 on 2021-01-22 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entry_management', '0001_initial'),
        ('item_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selected_Item_Info',
            fields=[
                ('item_id', models.ForeignKey(db_column='se_item', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='se_item', serialize=False, to='item_management.item_info')),
                ('selected_item_count', models.PositiveSmallIntegerField(verbose_name='개수')),
                ('author', models.ForeignKey(db_column='se_user', on_delete=django.db.models.deletion.CASCADE, related_name='se_user', to=settings.AUTH_USER_MODEL)),
                ('entry_id', models.ForeignKey(db_column='se_entry', on_delete=django.db.models.deletion.CASCADE, related_name='se_entry', to='entry_management.entry_info')),
            ],
        ),
        migrations.AddField(
            model_name='entry_info',
            name='author',
            field=models.ForeignKey(db_column='et_user', on_delete=django.db.models.deletion.CASCADE, related_name='et_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
