from django.conf.urls import url
from bundesinfo import views

app_name = 'bundesinfo'

urlpatterns = [
    url(r'standings/$', views.Standings.as_view(), name='standings'),
    url(r'next-round/$', views.NextRound.as_view(), name='next_round')
]
