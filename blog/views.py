from rest_framework import viewsets

from blog.models import Post
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import PostSerializer



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)