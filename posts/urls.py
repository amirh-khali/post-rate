from django.urls import path

from posts.views import *

urlpatterns = [
    path('', PostListView.as_view({'get': 'list', 'post': 'create'}), name='post'),
    path('rate/', RatingCreateUpdateView.as_view(), name='rate-post')
]