# Generated by Django 3.1.2 on 2020-12-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageUpload', '0002_auto_20201209_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Image'),
        ),
    ]
