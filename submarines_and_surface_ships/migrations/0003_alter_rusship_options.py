# Generated by Django 4.0 on 2022-01-07 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submarines_and_surface_ships', '0002_alter_rusship_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rusship',
            options={'ordering': ['-time_create', 'title'], 'verbose_name': 'корабль военно-морского флота России', 'verbose_name_plural': 'Корабли военно-морского флота России'},
        ),
    ]