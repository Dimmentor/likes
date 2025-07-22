from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from likes.videos.utils.serializers import LikeResponseSerializer
from likes.videos.utils.services import VideoService


class LikeAPIView(APIView):
    serializer_class = LikeResponseSerializer
    service = VideoService()

    @extend_schema(responses={201: None, 200: None})
    def post(self, request, video_id):
        success, message = self.service.handle_like(request.user, video_id)
        status_code = status.HTTP_201_CREATED if success else status.HTTP_400_BAD_REQUEST
        return Response({'message': message}, status=status_code)

    @extend_schema(responses={200: None, 404: None})
    def delete(self, request, video_id):
        success, message = self.service.handle_unlike(request.user, video_id)
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
