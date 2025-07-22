from django.db.models import F, Q
from likes.videos.models import Video, Like


class VideoRepository:
    def all(self):
        return Video.objects.select_related('owner').prefetch_related('files').all()

    def get_published(self):
        return Video.objects.filter(is_published=True).select_related('owner').prefetch_related('files')

    def get_published_or_owner(self, user):
        return Video.objects.filter(Q(is_published=True) | Q(owner=user)).select_related('owner').prefetch_related(
            'files')

    def get_for_update(self, video_id):
        return Video.objects.select_for_update().get(id=video_id)

    def increment_likes(self, video):
        Video.objects.filter(id=video.id).update(total_likes=F('total_likes') + 1)

    def decrement_likes(self, video):
        Video.objects.filter(id=video.id).update(total_likes=F('total_likes') - 1)


class LikeRepository:
    def exists(self, user, video):
        return Like.objects.filter(user=user, video=video).exists()

    def create(self, user, video):
        Like.objects.create(user=user, video=video)

    def delete(self, user, video):
        Like.objects.filter(user=user, video=video).delete()
