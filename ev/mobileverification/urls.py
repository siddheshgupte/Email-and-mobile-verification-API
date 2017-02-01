from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^_verification/$', views.SmsVerification, name="SMSVERIFICATION"),
    url(r'^_otp_verification/$', views.MobileOtpVerification, name="MOBILEOTPVERIFICATION"),
]