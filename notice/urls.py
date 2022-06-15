from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('api/', Bsc.as_view()),
    path('psc/', Psc.as_view()),
    path('fetchNotice', FetchNotice.as_view()),
    path('getjob', Getjob.as_view()),
]
