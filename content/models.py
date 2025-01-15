from django.db import models

# Create your models here.

# Justagram need DB Modeling

#Justagram feed
class Feed(models.Model):
    content = models.TextField() #TextDetail(글내용)
    image = models.TextField()  #FeedImage(피드이미지)
    profile_image = models.TextField() #profileimage(프로필이미지)
    user_id = models.IntegerField() #Author(글쓴이)
    like_count = models.IntegerField() #like count(좋아요 수)




