from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from apps.review.serializers import RatingSerializer, CommentSerializer
from apps.review.models import Rating, Comment

from apps.generals.permissions import IsOwner

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# class RatingDeleteView(generics.DestroyAPIView):
#     queryset = Rating.objects.all()
#     permission_classes = [IsAuthenticated ,IsOwner,]
#
#     def get_queryset(self):
#         return Rating.objects.filter(owner=self.request.user)
#
#
# class CommentDeleteView(generics.DestroyAPIView):
#     queryset = Comment.objects.all()
#     permission_classes = [IsAuthenticated, IsOwner, ]
#
#     def get_queryset(self):
#         return Comment.objects.filter(owner=self.request.user)