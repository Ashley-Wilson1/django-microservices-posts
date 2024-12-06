import random
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
import requests


# Create your views here.
class PostCommentAPIView(APIView):
    def get(self, _, pk=None):
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)

class CommentsAPIView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        comment = serializer.data

        if random.randint(1,10) <= 5:
            r = requests.post('http://127.0.0.1:8000/api/posts/%d/comments' % comment['post_id'], data={'text': comment['text']})

            if not r.ok:
                pass
            
        return Response(comment)