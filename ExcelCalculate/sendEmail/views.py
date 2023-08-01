from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def send(receiverEmail, verifyCode):
    try:
        content = {'verifyCode' : verifyCode}
        msg_html = render_to_string("sendEmail/email_format.html", content)
        msg = EmailMessage(subject = "[멀티캠퍼스] 인증 코드 발송 메일",
                            body = msg_html,
                            from_email = "chemical0128@gmail.com",
                            bcc = [receiverEmail])
        msg.content_subtype = "html"
        msg.send()

        print("sendEmail > views.py > send 함수 임무 완료------------------------")
        return True
    except:
        print("sendEmail > views.py > send 함수 임무 실패 원인 파악하세용!!-------")
        return False
    
    return HttpResponse("sendEmail, send function!")