from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, "main/index.html") # calculate에 session 어떻게 넘어가는지 확인
    else:
        return redirect('main_signin')
    # return render(request, "main/index.html")

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

def login(request):
    # 로그인 된 사용자만 이용할 수 있도록 구현
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']

    try:
        user = User.objects.get(user_email = loginEmail)
    except:
        return redirect('main_loginFail')
    
    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_loginFail')

def loginFail(request):
    return render(request, 'main/loginFail.html')

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
        # response.set_cookie('user', user)
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response

    else:
        return redirect('main_verifyCode')

    # return redirect('main_index')   # 인증이 완료되면 메인 화면으로 보내줌

def result(request):
    if 'user_name' in request.session.keys():
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']

        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']

        content['grade_df'] = request.session['grade_df']
        content['email_df'] = request.session['email.df']

        del request.session['grade_df']
        del request.session['email.df']
    
        # ------------------------------------------------------------------------

        content['grade_calculate_pd_dic'] = request.session['grade_calculate_pd_dic']

        del request.session['grade_calculate_pd_dic']
        
        return render(request, "main/result.html", content)
    else:
        return redirect('main_signin')

def logout(request):
    del request.session['user_name']
    del request.session['user_email']

    return redirect('main_signin')