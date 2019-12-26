from django.conf.urls import url
from bundesinfo import views

app_name = 'bundesinfo'

urlpatterns = [
    url(r'standings/$', views.Standings.as_view(), name='standings')
]
