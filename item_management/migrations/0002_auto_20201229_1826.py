# Generated by Django 3.1.3 on 2020-12-29 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_class',
            fields=[
                ('item_class', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='item_class')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item_condition',
            fields=[
                ('item_condition', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='item_condition')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=50)),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.IntegerField()),
                ('manager_name', models.CharField(max_length=50, null=True)),
                ('manu_name', models.CharField(max_length=50, null=True)),
                ('model_number', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(default='item_image/no_image.png', upload_to='item_image/%Y/%m/')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('item_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item_management.item_class', verbose_name='item_class')),
                ('item_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item_management.item_condition', verbose_name='item_condition')),
            ],
        ),
        migrations.DeleteModel(
            name='Item_management',
        ),
    ]
