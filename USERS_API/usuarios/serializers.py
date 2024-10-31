from rest_framework import serializers
from .models import Usuario, Perfiles, Pago

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class PerfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfiles
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    perfiles = PerfilesSerializer(many=True, read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'
