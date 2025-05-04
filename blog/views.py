from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Post
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import PostSerializer



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)