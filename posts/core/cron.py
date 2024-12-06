import json
from django.db import connections

from .models import Post


def sync_comments():
    comments = get_comments()

    posts =  Post.objects.all()

    for post in posts:
        post_comments = json.loads(post.comments)
        filtered_comments = [{
            "text":c["text"]
        } for c in comments if c['post_id']==post.id]

        if len(post_comments) < len(filtered_comments):
            post.comments =json.dumps(filtered_comments)
            post.save()

def get_comments():
    with connections['comments_db'].cursor() as cursor:
        cursor.execute('SELECT * FROM core_comment')

        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]