from django.urls import path
from . import views
app_name = 'firstapp'
urlpatterns = [
    #path('',views.form_name_view,name="form"),
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path("user_login/",views.user_login,name="user_login")
    #path('/',views.other,name="other"),
    #path('',views.users,name='users')
]

