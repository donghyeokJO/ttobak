
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls), #Django-admin을 통해 관리할 수 있도록 추가해줌.
    path('api/',include('tt_apis.urls')), #tt_apis app에서 만들어준 url route적용
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
