# Generated by Django 5.2.2 on 2025-06-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialNewton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_id', models.IntegerField()),
                ('usuario_nombre', models.CharField(max_length=100)),
                ('puntos_x', models.TextField()),
                ('puntos_y', models.TextField()),
                ('polinomio', models.TextField()),
                ('valor_evaluado', models.FloatField(blank=True, null=True)),
                ('resultado', models.FloatField(blank=True, null=True)),
                ('pasos', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
