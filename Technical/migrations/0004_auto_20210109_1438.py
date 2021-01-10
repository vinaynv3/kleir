# Generated by Django 3.1.2 on 2021-01-09 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Technical', '0003_actualbua_areadetails_deviations_fairmarketvalue_finalnotes_permissiblebua_propertystatus_rate_sanct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fairmarketvalue',
            name='Date',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='fairmarketvalue',
            name='Distressed',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='fairmarketvalue',
            name='GovtValue',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='finalnotes',
            name='IsInDemolitionList',
            field=models.BooleanField(verbose_name=' Property in Demolition list ?'),
        ),
        migrations.AlterField(
            model_name='finalnotes',
            name='IsNegative',
            field=models.BooleanField(verbose_name=' Property in bad community ?'),
        ),
        migrations.AlterField(
            model_name='finalnotes',
            name='ValuationDoneEarlier',
            field=models.BooleanField(verbose_name=' Validation Done Earlier ?'),
        ),
    ]
