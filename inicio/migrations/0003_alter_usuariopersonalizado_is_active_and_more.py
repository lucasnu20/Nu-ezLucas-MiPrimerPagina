# Generated by Django 5.1.5 on 2025-02-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0002_alter_receta_descripcion_alter_receta_ingredientes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
