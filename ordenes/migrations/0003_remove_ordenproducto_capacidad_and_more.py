# Generated by Django 5.0.6 on 2024-07-11 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0002_alter_orden_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenproducto',
            name='capacidad',
        ),
        migrations.RemoveField(
            model_name='ordenproducto',
            name='color',
        ),
        migrations.RemoveField(
            model_name='ordenproducto',
            name='largo',
        ),
        migrations.RemoveField(
            model_name='ordenproducto',
            name='tipo',
        ),
    ]
