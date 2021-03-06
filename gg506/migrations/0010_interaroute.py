# Generated by Django 2.1.5 on 2019-03-25 00:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gg506', '0009_auto_20190318_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteraRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_distance', models.FloatField(default=0.0)),
                ('total_time', models.FloatField(default=0.0)),
                ('total_cost', models.FloatField(default=0.0)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('da', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gg506.Da')),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gg506.Hub')),
            ],
        ),
    ]
