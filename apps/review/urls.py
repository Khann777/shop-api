from django.urls import path

from apps.review.views import  RatingCreateView, CommentCreateView

urlpatterns = [
    # path('rating-delete/<int:pk>/', RatingDeleteView.as_view(), name='rating-delete'),
    path('rating-create/', RatingCreateView.as_view(), name='rating-create'),
    # path('comment-delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment-create/', CommentCreateView.as_view(), name='comment-create'),
]