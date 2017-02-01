from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$', views.EmailVerification, name="EMAILVERIFICATION"),
    url(ur'^_link/(?P<encrypted_email_id>.*)/(?P<verification_code>.*)/$', views.EmailVerificationLink, name="EMAILVERIFICATIONLINK"),
]