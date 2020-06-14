from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from app.pkg.account.api import serializers

User = get_user_model()


# ****************************************************************************
# COMMON VIEWS
# ****************************************************************************

class ActionView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = None
    status_code = status.HTTP_200_OK

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=self.status_code, headers=headers)


# ****************************************************************************
# LOGIN VIEW
# ****************************************************************************

class LoginView(ActionView):
    serializer_class = serializers.LoginSerializer


# ****************************************************************************
# CHANGE PASSWORD VIEW
# ****************************************************************************

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('put',)

    def get_object(self):
        return self.request.user

