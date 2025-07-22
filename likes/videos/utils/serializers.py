from rest_framework import serializers
from likes.videos.models import Video, VideoFile, Like


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ('file', 'quality')


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ('id', 'owner', 'name', 'total_likes', 'created_at', 'files')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'video', 'created_at')
        read_only_fields = ('user', 'created_at')


class LikeResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class StatisticsSerializer(serializers.Serializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()
