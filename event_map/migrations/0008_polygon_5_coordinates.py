# Generated by Django 3.1.7 on 2023-04-30 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_map', '0007_auto_20230201_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Polygon_5_Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=None, verbose_name='Широта')),
                ('longitude', models.FloatField(default=None, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'крайняя кордината желтой области СПЧ-5',
                'verbose_name_plural': 'Область вызова СПЧ-5',
            },
        ),
    ]
