from django.urls import path

from posts.views import *

urlpatterns = [
    path('user/<int:user_id>/', PostListView.as_view({'get': 'list', 'post': 'create'}), name='post'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post')
]