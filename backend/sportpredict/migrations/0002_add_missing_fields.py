from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportpredict', '0001_initial'),
    ]

    operations = [
        # Usuario: add racha_actual, mejor_racha
        migrations.AddField(
            model_name='usuario',
            name='racha_actual',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usuario',
            name='mejor_racha',
            field=models.IntegerField(default=0),
        ),
        # Deporte: add icono, descripcion
        migrations.AddField(
            model_name='deporte',
            name='icono',
            field=models.CharField(blank=True, default='🏆', max_length=50),
        ),
        migrations.AddField(
            model_name='deporte',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        # Equipo: add activo
        migrations.AddField(
            model_name='equipo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        # Usuario: add tipo_suscripcion (might be missing from initial migration)
        migrations.AddField(
            model_name='usuario',
            name='tipo_suscripcion',
            field=models.CharField(
                choices=[('FREE', 'Free'), ('PREMIUM', 'Premium')],
                default='FREE',
                max_length=10,
            ),
        ),
    ]
