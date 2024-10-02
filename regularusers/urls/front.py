from django.urls import path, include

from regularusers.views.front import (
    FrontLoginViaOtpView,
    UserRegisterView,
    CurrentUserView,
    UserLogoutView
)


urlpatterns = [
    path("users/send-otp" ,   FrontLoginViaOtpView.as_view() , name="sendOtp"),
    path("users/verify-otp" , FrontLoginViaOtpView.as_view() , name="verifyOtp"),
    path('users/register' , UserRegisterView.as_view() , name="userRegister"),
    path("users/logout" , UserLogoutView.as_view() , name="logoutUser"),
    path("users/user" , CurrentUserView.as_view() , name="getUser")
]