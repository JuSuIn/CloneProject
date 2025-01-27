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
        email = request.session.get('email', None)  # request.session['email'] # session
        user = User.objects.filter(email=email).first()  # now login user information

        # print(feed_list)
        # feed print
        # for feed in feed_list:
        #     print(feed.content)

        # print(" 로그인한 사용자 : ",request.session['email'])

        # print("확실히 제대로 되고 있는건가?!",user.profile_image)
        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")


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


            like_count=Like.objects.filter(feed_id=feed.id,is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id,email=email,is_like=True).exists()
            is_marked = BookMark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

            #print('like 확인중 ',is_liked)

            feed_list.append(dict(id=feed.id,
                                  content=feed.content,
                                  image=feed.image,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  like_count=like_count,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked,
                                  ))


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


        # my only click feed List ----------------------------------------------------------------------

        # Filter only the feeds I wrote related to my profile
        feed_list=Feed.objects.filter(email=email).all()
        #Call the feed ID to display only the lists
        # that you have liked related to your profile.
        like_list = list(Like.objects.filter(email=email,is_like=True).values_list('feed_id',flat=True))
        # Print only the list of likes included in the feed
        like_feed_list =  Feed.objects.filter(id__in=like_list)

        # Among the ways to retrieve profile-related bookmarks,
        # I first retrieve a list of the feed IDs of the bookmarks I clicked on.
        bookmark_list = list(BookMark.objects.filter(email=email, is_marked=True).values_list('feed_id',flat=True))
        # Filters a feed and retrieves a list of bookmarks from the feed.
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)

        #print(like_list)
        # ------------------------------------------------------------------------------------------------

        return render(request,"content/profile.html",
                      context=dict(feed_list=feed_list,
                                   like_feed_list=like_feed_list,
                                   bookmark_feed_list=bookmark_feed_list,
                                   user=user))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)

        email = request.session.get('email', None)  # request.session['email'] # session

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content,email=email)

        return Response(status=200)

class ToogleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text',True)
        email = request.session.get('email', None)
        #email = request.data.get('email', None)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False

        like=Like.objects.filter(feed_id=feed_id,email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id,is_like=is_like,email=email)

        return Response(status=200)

class ToogleBookMark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        email = request.session.get('email', None)
        # email = request.data.get('email', None)

        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False

        bookmark = BookMark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            BookMark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)