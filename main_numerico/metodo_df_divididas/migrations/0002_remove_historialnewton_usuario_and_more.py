# Generated by Django 5.2.2 on 2025-06-15 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metodo_df_divididas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialnewton',
            name='usuario',
        ),
        migrations.AddField(
            model_name='historialnewton',
            name='usuario_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialnewton',
            name='usuario_nombre',
            field=models.CharField(default='Invitado', max_length=100),
            preserve_default=False,
        ),
    ]
