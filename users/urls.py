from django.conf.urls import url
from views import LoginClass
from views import RegisterClass
from views import logout

app_name = 'user'

urlpatterns = [
	url(r'users/sign_in/$', LoginClass.as_view(), name = 'login'),
	url(r'users/sign_up/$', RegisterClass.as_view(), name = 'signup'),
	url(r'users/logout/$', logout, name = 'logout'),
	
]