from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    pass
    # profile picture
    """
        **** userprofile ***
        user_id,   -> 화면에 표기 되는 사용자 아이디
        user_name  -> 화면에 표시 되는 사용자 이름 
        user_email -> 회원가입 할때 사용 하는 아이디
        user_password ->  유저 비밀번호  -> default 꺼 씀
    """

    profile_image = models.TextField() # 프로필 이미지
    nickname = models.CharField(max_length=24,unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'


    class Meta:
        db_table = 'User'
