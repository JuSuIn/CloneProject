from pyexpat.errors import messages

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password

class Join(APIView):
    def get(self,request):
        return render(request,'user/join.html')

    def post(self,request):
        #todoImplementation
        email = request.data.get('email',None)
        nickname = request.data.get('nickname',None)
        name = request.data.get('name',None)
        password = request.data.get('password',None)

        #아래에 유저에 데이터를 집어 넣을 때 패스워드는 암호화를 해서 집어 넣어야 됨
        #(When entering user data below, the password must be encrypted.)
        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status=200)


class Login(APIView):
    def get(self,request):
        return render(request,"user/login.html")


    def post(self,request):
        #todo Login
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user=User.objects.filter(email=email).first() # querySet, only first

        #print(user.check_password(password))

        # todo no data Error return
        if user is None:
            return Response(status=404,data=dict(messages="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # todo login ,session and quki

            request.session['email'] = email

            return Response(status=200)
        else:
            return Response(status=400,data=dict(messages="회원정보가 잘못되었습니다."))


class Logout(APIView):
    def get(self,request):
        print("안되낭?!?!?!?")
        request.session.flush()
        return render(request,"user/login.html")


