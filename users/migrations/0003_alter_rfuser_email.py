# Generated by Django 4.2.18 on 2025-02-09 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_rfuser_render_coin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
