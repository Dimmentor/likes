import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from likes.videos.models import Video, VideoFile

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    '''Генерация 10к пользователей, 100000 страниц с видео, 200000 видео-файлов'''

    def handle(self, *args, **options):
        self.stdout.write("Creating users")
        users = []
        for i in range(1, 10001):
            users.append(User(
                username=f'user_{i}',
                email=f'user_{i}@yandex.ru',
                password='secret_password123'
            ))
        User.objects.bulk_create(users)
        self.stdout.write(f"Created {len(users)} users")

        self.stdout.write("Creating videos")
        videos = []
        qualities = ['HD', 'FHD', 'UHD']
        for i in range(1, 100001):
            owner = random.choice(users)
            videos.append(Video(
                owner=owner,
                is_published=random.choice([True, False]),
                name=fake.sentence(nb_words=3),
                total_likes=random.randint(0, 1000)
            ))
        Video.objects.bulk_create(videos)
        self.stdout.write(f"Created {len(videos)} videos")

        self.stdout.write("Creating video files")
        video_files = []
        for video in Video.objects.all():
            for quality in random.sample(qualities, random.randint(1, 3)):
                video_files.append(VideoFile(
                    video=video,
                    file=f'videos/{video.id}_{quality}.mp4',
                    quality=quality
                ))
        VideoFile.objects.bulk_create(video_files)
        self.stdout.write(f"Created {len(video_files)} video files")

        self.stdout.write(self.style.SUCCESS("Successfully generated test data"))
