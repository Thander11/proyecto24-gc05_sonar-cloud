from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Usuario, Perfiles, Pago
from .serializers import UsuarioSerializer, PerfilesSerializer, PagoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        query = request.query_params.get('q')
        print(query)
        if query:
            usuarios = Usuario.objects.filter(
                correoelectronico__icontains=query
            ) | Usuario.objects.filter(
                nombreusuario__icontains=query
            )
            if query.isdigit():
                usuarios = usuarios| Usuario.objects.filter(
                    id=query)
            serializer = self.get_serializer(usuarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get usuario por ID
    def retrieve(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Update usuario por ID
    def update(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
            serializer = UsuarioSerializer(usuario, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Delete usuario por ID
    def destroy(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    # Get lista de pagos por idUsuario
    @action(detail=False, methods=['get'])
    def por_usuario(self, request, idUsuario=None):
        pagos = Pago.objects.filter(idusuario=idUsuario)
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Get pago por ID de pago
    def retrieve(self, request, pk=None):
        try:
            pago = Pago.objects.get(pk=pk)
            serializer = PagoSerializer(pago)
            return Response(serializer.data)
        except Pago.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Update pago por ID de pago
    def update(self, request, pk=None):
        try:
            pago = Pago.objects.get(pk=pk)
            serializer = PagoSerializer(pago, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pago.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Delete pago por ID de pago
    def destroy(self, request, pk=None):
        try:
            pago = Pago.objects.get(pk=pk)
            pago.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Pago.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PerfilesViewSet(viewsets.ModelViewSet):
    queryset = Perfiles.objects.all()
    serializer_class = PerfilesSerializer

    # Get lista de perfiles por idUsuario
    @action(detail=False, methods=['get'])
    def por_usuario(self, request, idUsuario=None):
        perfiles = Perfiles.objects.filter(idusuario=idUsuario)
        serializer = self.get_serializer(perfiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Get perfil por ID de perfil
    def retrieve(self, request, pk=None):
        try:
            perfil = Perfiles.objects.get(pk=pk)
            serializer = PerfilesSerializer(perfil)
            return Response(serializer.data)
        except Perfiles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Update perfil por ID de perfil
    def update(self, request, pk=None):
        try:
            perfil = Perfiles.objects.get(pk=pk)
            serializer = PerfilesSerializer(perfil, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Perfiles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Delete perfil por ID de perfil
    def destroy(self, request, pk=None):
        try:
            perfil = Perfiles.objects.get(pk=pk)
            perfil.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfiles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
