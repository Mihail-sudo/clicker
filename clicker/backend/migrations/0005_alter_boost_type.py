# Generated by Django 4.0.4 on 2022-06-13 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_boost_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boost',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'casual'), (1, 'auto')], default=0),
        ),
    ]
