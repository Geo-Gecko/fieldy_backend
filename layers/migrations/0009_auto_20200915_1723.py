# Generated by Django 3.1 on 2020-09-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0008_shuserdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointlayer',
            name='field_id',
            field=models.UUIDField(unique=True),
        ),
        migrations.AlterField(
            model_name='polygonlayer',
            name='field_id',
            field=models.UUIDField(unique=True),
        ),
    ]
