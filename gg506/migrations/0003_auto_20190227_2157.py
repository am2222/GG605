# Generated by Django 2.1.5 on 2019-02-27 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gg506', '0002_auto_20190227_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='mode',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.DeleteModel(
            name='Mode',
        ),
    ]
