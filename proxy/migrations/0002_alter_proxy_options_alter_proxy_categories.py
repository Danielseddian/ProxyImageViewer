# Generated by Django 4.2.4 on 2023-08-16 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proxy',
            options={'ordering': ['-amount'], 'verbose_name': 'Прокси', 'verbose_name_plural': 'Прокси'},
        ),
        migrations.AlterField(
            model_name='proxy',
            name='categories',
            field=models.ManyToManyField(related_name='proxies', to='proxy.category', verbose_name='Категории'),
        ),
    ]
