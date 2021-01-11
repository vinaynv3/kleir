# Generated by Django 3.1.2 on 2020-12-25 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PropertyDocs', '0006_auto_20201219_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Approach_Road', models.BooleanField()),
                ('Sewer_system', models.BooleanField()),
                ('Water_supply', models.BooleanField()),
                ('Electricity', models.BooleanField()),
                ('Construction_quality', models.BooleanField()),
                ('No_of_lifts', models.CharField(max_length=200)),
                ('connection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PropertyDocs.bankref')),
            ],
            options={
                'db_table': 'LayoutInfrastructure',
            },
        ),
        migrations.CreateModel(
            name='AsPerPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('East_to_west_in_Feet', models.PositiveIntegerField()),
                ('North_to_South_in_Feet', models.PositiveIntegerField()),
                ('Land_area_or_UDS_in_SFT', models.PositiveIntegerField()),
                ('Carpet_area_of_flat_in_SFT', models.PositiveIntegerField()),
                ('SBUA_of_Flat_in_SFT', models.PositiveIntegerField()),
                ('connection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PropertyDocs.bankref')),
            ],
            options={
                'db_table': 'PlotAreaPlan',
            },
        ),
        migrations.CreateModel(
            name='AsPerDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('East_to_west_in_Feet', models.PositiveIntegerField()),
                ('North_to_South_in_Feet', models.PositiveIntegerField()),
                ('Land_area_or_UDS_in_SFT', models.PositiveIntegerField()),
                ('Carpet_area_of_flat_in_SFT', models.PositiveIntegerField()),
                ('SBUA_of_Flat_in_SFT', models.PositiveIntegerField()),
                ('connection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PropertyDocs.bankref')),
            ],
            options={
                'db_table': 'PlotAreaDocuments',
            },
        ),
        migrations.CreateModel(
            name='Actuals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('East_to_west_in_Feet', models.PositiveIntegerField()),
                ('North_to_South_in_Feet', models.PositiveIntegerField()),
                ('Land_area_or_UDS_in_SFT', models.PositiveIntegerField()),
                ('Carpet_area_of_flat_in_SFT', models.PositiveIntegerField()),
                ('SBUA_of_Flat_in_SFT', models.PositiveIntegerField()),
                ('connection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PropertyDocs.bankref')),
            ],
            options={
                'db_table': 'PlotAreaActuals',
            },
        ),
    ]