# Generated by Django 4.0 on 2022-01-07 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submarines_and_surface_ships', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rusship',
            options={'ordering': ['-time_create', 'title'], 'verbose_name': 'корабли военно-морского флота России', 'verbose_name_plural': 'Корабли военно-морского флота России'},
        ),
    ]
