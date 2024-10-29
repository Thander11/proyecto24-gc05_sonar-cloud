from django.db import models

class Usuario(models.Model):
    correoelectronico = models.TextField(db_column='correoElectronico', unique=True)
    contrasena = models.TextField()
    nombreusuario = models.TextField(db_column='nombreUsuario')

    class Meta:
        managed = False
        db_table = 'Usuario'

class Pago(models.Model):
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario', related_name='pagos', blank=True)
    numerotarjeta = models.TextField(db_column='numeroTarjeta')
    fechacaducidad = models.TextField(db_column='fechaCaducidad')
    cvc = models.TextField()

    class Meta:
        managed = False
        db_table = 'Pago'

class Perfiles(models.Model):
    idperfil = models.AutoField(db_column='idPerfil', primary_key=True, blank=True)
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario', related_name='perfiles')
    nombreperfil = models.TextField(db_column='nombrePerfil')
    fotoperfil = models.IntegerField(db_column='fotoPerfil', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Perfiles'
