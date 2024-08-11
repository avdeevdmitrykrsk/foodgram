# Thirdparty imports
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Projects imports
from users.serializers import AvatarSerializer, UserSerializer

User = get_user_model()


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AvatarSerializer
    http_method_names = ('put', 'delete')
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        self.get_object().avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
