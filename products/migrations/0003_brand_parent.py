# Generated by Django 3.1.3 on 2020-12-15 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', related_query_name='child', to='products.brand', verbose_name='Parent'),
        ),
    ]