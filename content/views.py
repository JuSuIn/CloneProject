from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed,Reply,Like,BookMark
import os
from Justagram.settings import MEDIA_ROOT
from uuid import uuid4
from user.models import User


# Create your views here.
class Main(APIView):
    def get(self, request):

        feed_object_list = Feed.objects.all().order_by('-id') # select * from content_feed; , querySet
        feed_list = []

        email=''
        user=''

        for feed in feed_object_list:
            email=feed.email
            user=User.objects.filter(email=email).first()

            #reply list function add
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()

                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))

            #print('찾는지 테스트',user.nickname)
            feed_list.append(dict(id=feed.id,
                                  content=feed.content,
                                  image=feed.image,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  likes_count=feed.like_count,
                                  reply_list=reply_list
                                  ))

        email = request.session.get('email',None) #request.session['email'] # session
        user = User.objects.filter(email=email).first() # now login user information


        # print(feed_list)
        # feed print
        # for feed in feed_list:
        #     print(feed.content)

       # print(" 로그인한 사용자 : ",request.session['email'])

        #print("확실히 제대로 되고 있는건가?!",user.profile_image)
        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        return render(request,"Justagram/main.html",context=dict(feeds=feed_list,user=user))

#feed file upload
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
        #user_id =request.data.get('user_id')
        #profile_image =request.data.get('profile_image')
        email=request.session.get('email',None)

        Feed.objects.create(image=image,content=content,email=email)
        #Feed.objects.create(image=image,content=content,user_id=user_id,profile_image=profile_image,like_count=0)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        #print("test!!!");
        email = request.session.get('email', None)  # request.session['email'] # session
        user = User.objects.filter(email=email).first()  # now login user information

        # print("확실히 제대로 되고 있는건가?!",user.profile_image)
        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")

        return render(request,"content/profile.html",context=dict(user=user))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)

        email = request.session.get('email', None)  # request.session['email'] # session

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content,email=email)

        return Response(status=200)
