from django.urls import path, include
from rest_framework.routers import DefaultRouter
from likes.videos.views.videos import VideoViewSet
from likes.videos.views.likes import LikeAPIView
from likes.videos.views.statistics import StatisticsSubqueryAPIView, StatisticsGroupByAPIView

router = DefaultRouter()
router.register(r'', VideoViewSet, basename='video')

urlpatterns = [
    path('<int:video_id>/likes/', LikeAPIView.as_view(), name='video-likes'),
    path('statistics-subquery/', StatisticsSubqueryAPIView.as_view(), name='statistics-subquery'),
    path('statistics-group-by/', StatisticsGroupByAPIView.as_view(), name='statistics-group-by'),
]

urlpatterns += router.urls