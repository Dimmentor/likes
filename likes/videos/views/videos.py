from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from likes.videos.utils.serializers import VideoSerializer
from likes.videos.views.likes import VideoService


class VideoListAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        service = VideoService()
        return service.get_videos_for_user(self.request.user)


class VideoDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        service = VideoService()
        return service.get_videos_for_user(self.request.user)


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        service = VideoService()
        return service.get_videos_for_user(self.request.user) \
            .select_related('owner') \
            .prefetch_related('files') \
            .order_by('-created_at')

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def ids(self, request):
        service = VideoService()
        video_ids = service.get_published_video_ids()
        return Response(video_ids)
