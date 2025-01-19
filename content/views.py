from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
import os
from Justagram.settings import MEDIA_ROOT
from uuid import uuid4

# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id') # select * from content_feed; , querySet
        # print(feed_list)
        # feed print
        # for feed in feed_list:
        #     print(feed.content)
        return render(request,"Justagram/main.html",context=dict(feeds=feed_list))

#file upload
class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # file = request.data.get('file')
        image =uuid_name
        # image =request.data.get('image')
        content =request.data.get('content')
        user_id =request.data.get('user_id')
        profile_image =request.data.get('profile_image')

        Feed.objects.create(image=image,content=content,user_id=user_id,profile_image=profile_image,like_count=0)

        return Response(status=200)



