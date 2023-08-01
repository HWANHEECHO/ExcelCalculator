from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def signup(request):
    return render(request, "main/signup.html")

def join(request):
    print("테스트", request)

    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    # print("사용자 정보 저장 완료됨!!")

    code = randint(1000, 9000)
    print("인증코드 생성----------------------------", code)

    response = redirect('main_verifyCode')
    response.set_cookie('code', code)
    response.set_cookie('user_id', user.id)

    print("응답 객체 완성---------------------------", response)

    send_result = send(email, code)
    if send_result:
        print("main > views.py > 이메일 발송 중 완료된 것 같음...")
        return response
    else:
        return HttpResponse("이메일 발송 실패!")

def signin(request):
    return render(request, "main/signin.html")

def verifyCode(request):
    return render(request, "main/verifyCode.html")

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    print("코드 확인: ", user_code, cookie_code)

    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()

        print("DB에 user_validate 업데이트--------------------------")

        response = redirect('main_index')

        response.delete_cookie('code')
        response.delete_cookie('user_id')
        response.set_cookie('user', user)

        return response

    else:
        return redirect('main_verifyCode')

    # return redirect('main_index')   # 인증이 완료되면 메인 화면으로 보내줌

def result(request):
    return render(request, "main/result.html")