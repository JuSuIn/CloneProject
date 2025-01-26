from django.db import models

# Create your models here.

# Justagram need DB Modeling

#Justagram feed
class Feed(models.Model):
    content = models.TextField() #TextDetail(글내용)
    image = models.TextField()  #FeedImage(피드이미지)
   # profile_image = models.TextField(default='') #profileimage(프로필이미지)
   # nickname= models.TextField(default='')  #Author(글쓴이)
    # user_id = models.TextField() #Author(글쓴이)
    email = models.EmailField(default='') #email(이메일)
    like_count = models.IntegerField(default=0) #like count(좋아요 수)

# like count
class Like(models.Model):
   feed_id = models.IntegerField(default=0)
   email = models.EmailField(default='')
   is_like = models.BooleanField(default=True) #update 위한 flag

#comment
class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

#bookmark
class BookMark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=False)




