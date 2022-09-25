from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, Follow
from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, \
    FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     super(PostViewSet, self).perform_update(serializer)
    #
    # def perform_destroy(self, serializer):
    #     if serializer.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     super(CommentViewSet, self).perform_update(serializer)
    #
    # def perform_destroy(self, serializer):
    #     if serializer.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     super(CommentViewSet, self).perform_destroy(serializer)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

