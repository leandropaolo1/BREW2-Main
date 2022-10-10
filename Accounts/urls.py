from Accounts.views import (
     CustomUserRegister,
     CustomeUserLogin,
    )
from django.urls import path
app_name = 'Accounts'

urlpatterns = [

    path('register/', CustomUserRegister.as_view(), name="register_user"),
    path('login/', CustomeUserLogin.as_view(), name="login_user"),

]