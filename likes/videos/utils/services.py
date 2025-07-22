from django.db import transaction
from django.db.models import Q
from likes.users.models import User
from likes.videos.models import Video
from likes.videos.utils.repositories import VideoRepository, LikeRepository


class VideoService:
    def __init__(self):
        self.video_repo = VideoRepository()
        self.like_repo = LikeRepository()

    def get_videos_for_user(self, user):
        queryset = Video.objects.all()
        if not user.is_staff:
            if user.is_authenticated:
                queryset = queryset.filter(Q(is_published=True) | Q(owner=user))
            else:
                queryset = queryset.filter(is_published=True)
        return queryset

    def get_published_video_ids(self):
        return list(
            self.video_repo.get_published()
            .values_list('id', flat=True)
        )

    @transaction.atomic
    def handle_like(self, user: User, video_id: int) -> tuple[bool, str]:
        video = self.video_repo.get_for_update(video_id)
        if not video.is_published:
            return False, "Video is not published"

        if self.like_repo.exists(user, video):
            return False, "Already liked"

        self.like_repo.create(user, video)
        self.video_repo.increment_likes(video)
        return True, "Liked successfully"

    @transaction.atomic
    def handle_unlike(self, user: User, video_id: int) -> tuple[bool, str]:
        video = self.video_repo.get_for_update(video_id)

        if not self.like_repo.exists(user, video):
            return False, "Like does not exist"

        self.like_repo.delete(user, video)
        self.video_repo.decrement_likes(video)
        return True, "Like successfully removed"
