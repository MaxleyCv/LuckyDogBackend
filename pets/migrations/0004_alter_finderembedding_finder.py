# Generated by Django 5.0.3 on 2024-03-24 01:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_finder_pet_type_searcher_pet_type_finderembedding_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finderembedding',
            name='finder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.finder'),
        ),
    ]
