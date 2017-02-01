
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^email_verification', include('emailverification.urls')),
    url(r'^sms', include('mobileverification.urls')),
    url(r'^mobile', include('mobileverification.urls'))

]
