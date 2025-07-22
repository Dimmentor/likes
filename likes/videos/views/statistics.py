from django.db.models import OuterRef, Subquery, Sum
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from likes.users.models import User
from likes.videos.models import Video
from likes.videos.utils.serializers import StatisticsSerializer


class StatisticsSubqueryAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StatisticsSerializer

    @extend_schema(responses={200: StatisticsSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        subquery = Video.objects.filter(
            is_published=True,
            owner_id=OuterRef('id')
        ).values('owner_id').annotate(
            likes_sum=Sum('total_likes')
        ).values('likes_sum')

        users = User.objects.annotate(
            likes_sum=Subquery(subquery)
        ).order_by('-likes_sum').values('username', 'likes_sum')

        return Response(list(users))


class StatisticsGroupByAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StatisticsSerializer

    @extend_schema(responses={200: StatisticsSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(
            videos__is_published=True
        ).annotate(
            likes_sum=Sum('videos__total_likes')
        ).order_by('-likes_sum').values('username', 'likes_sum')

        return Response(list(users))
