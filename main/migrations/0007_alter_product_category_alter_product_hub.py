# Generated by Django 5.2 on 2025-04-15 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_category_slug_alter_hub_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='main.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='hub',
            field=models.ManyToManyField(blank=True, to='main.hub'),
        ),
    ]
