# Generated by Django 3.1.7 on 2023-02-01 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_map', '0006_polygon_1_coordinates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Polygon_2_Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=None, verbose_name='Широта')),
                ('longitude', models.FloatField(default=None, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'крайняя кордината желтой области СПЧ-2',
                'verbose_name_plural': 'Область вызова СПЧ-2',
            },
        ),
        migrations.CreateModel(
            name='Polygon_3_Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=None, verbose_name='Широта')),
                ('longitude', models.FloatField(default=None, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'крайняя кордината желтой области СПЧ-3',
                'verbose_name_plural': 'Область вызова СПЧ-3',
            },
        ),
        migrations.CreateModel(
            name='Polygon_4_Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default=None, verbose_name='Широта')),
                ('longitude', models.FloatField(default=None, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'крайняя кордината желтой области СПЧ-4',
                'verbose_name_plural': 'Область вызова СПЧ-4',
            },
        ),
        migrations.AlterModelOptions(
            name='polygon_1_coordinates',
            options={'verbose_name': 'крайняя кордината желтой области СПЧ-1', 'verbose_name_plural': 'Область вызова СПЧ-1'},
        ),
    ]
