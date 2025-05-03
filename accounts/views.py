from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Method "GET" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
