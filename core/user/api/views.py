from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from ..models import User
from .serializers import UserSerializer


# class AddressApiViewSet(ModelViewSet):
#     Permission_classes = [IsAuthenticated]
#     serializer_class = AddressSerializer
#     queryset = Address.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['user_id', 'active']


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        password = request.data['password']
        if password:
            request.data['password'] = make_password(password)
        else:
            request.data['password'] = request.user.password
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
