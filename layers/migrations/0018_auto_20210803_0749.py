# Generated by Django 3.1 on 2021-08-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0017_auto_20210317_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolygonJsonLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('field_id', models.UUIDField(unique=True)),
                ('user_id', models.CharField(max_length=30)),
                ('properties', models.JSONField(blank=True, default=dict)),
                ('geometry', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.DeleteModel(
            name='FieldIndicators',
        ),
        migrations.DeleteModel(
            name='PointLayer',
        ),
    ]
