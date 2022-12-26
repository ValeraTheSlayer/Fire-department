# Generated by Django 4.0.4 on 2022-05-09 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department_structure', '0001_initial'),
        ('personnel', '0001_initial'),
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentEmergency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_call_start', models.DateTimeField(blank=True, null=True, verbose_name='Время начала звонка')),
                ('date_of_call_end', models.DateTimeField(blank=True, null=True, verbose_name='Время конца звонка')),
                ('income_call_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер тел. заявителя')),
                ('income_call_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='ФИО заявителя')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Адрес')),
                ('object_owner', models.CharField(blank=True, max_length=100, null=True, verbose_name='Владелец объекта')),
                ('emergency_closed', models.BooleanField(default=False, verbose_name='Вызов закрыть')),
                ('first_info_burning', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Первичная информация по сообщению')),
                ('department', models.ManyToManyField(to='department_structure.firedepartment', verbose_name='Пожарная часть')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Поступившие заявки',
            },
        ),
        migrations.CreateModel(
            name='DefaultEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Cобытие')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'Список частых событий (для журнала событий)',
            },
        ),
        migrations.CreateModel(
            name='EmergencyRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Ранг',
                'verbose_name_plural': 'Ранги',
            },
        ),
        migrations.CreateModel(
            name='EmergencyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
            },
        ),
        migrations.CreateModel(
            name='ObjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Категория объекта',
                'verbose_name_plural': 'Категории объекта',
            },
        ),
        migrations.CreateModel(
            name='JournalEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(blank=True, max_length=500, null=True, verbose_name='Событие')),
                ('date_insert', models.DateTimeField(verbose_name='Время')),
                ('emergency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emergency.currentemergency', verbose_name='Выезд - Текущие')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'Журнал событий',
            },
        ),
        migrations.AddField(
            model_name='currentemergency',
            name='emergency_rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emergency.emergencyrank', verbose_name='Ранг выезда'),
        ),
        migrations.AddField(
            model_name='currentemergency',
            name='emergency_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emergency.emergencytype', verbose_name='Тип выезда'),
        ),
        migrations.AddField(
            model_name='currentemergency',
            name='object_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emergency.objectcategory', verbose_name='Категория объекта'),
        ),
        migrations.AddField(
            model_name='currentemergency',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personnel.staff', verbose_name='Руководитель тушение пожара'),
        ),
        migrations.AddField(
            model_name='currentemergency',
            name='transport',
            field=models.ManyToManyField(blank=True, to='transport.transport', verbose_name='Привлеченные силы и средства'),
        ),
    ]
