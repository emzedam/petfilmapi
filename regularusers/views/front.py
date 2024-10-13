from django.shortcuts import render
from rest_framework import viewsets
from regularusers.models import (User , OTPRequest)
from rest_framework.views import APIView
from regularusers.services.snedOtp import SendOtpCode
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from regularusers.serializers import (
    RequestOtpSerializer,
    ResponseOtpRequestSerializer,
    VerifyOtpRequestSerializer,
    ObtainTokenSerializer,
    UserRegisterSerializer,
    UserSerializer
)

# Create your views here.


class FrontLoginViaOtpView(APIView):
    
    def get(self , request):
        serializer = RequestOtpSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            
            userExist = User.objects.filter(phone_number=data['receiver']).exists()
            if not userExist:
                return Response({"message" : "شماره همراه در سیستم یافت نشد. ابتدا ثبت نام کنید"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                otp = OTPRequest.objects.generate(data)
                
                sendOtp = SendOtpCode(receiver=otp.receiver , password=otp.password)
                if data['channel'] == 'Phone':
                    sendOtp.send_by_sms()
                elif data['channel'] == 'E-Mail':
                    sendOtp.send_by_email()   
                else:
                    return Response({"message": "کانال مربوط به ارسال کد معتبر نمیباشد"}, status=status.HTTP_400_BAD_REQUEST)
                         
                return Response(data=ResponseOtpRequestSerializer(otp).data , status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "خطایی در روند ارسال کد رخ داد !"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "خطایی رخ داد . ساختار و فرمت موبایل را رعایت کنید"} , status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self , request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_verify(data):
                try: 
                    user = User.objects.filter(phone_number=data['receiver']).first()
                    if user:
                        refresh = RefreshToken.for_user(user)
                        user.verified = True
                        user.save()
                        return Response({
                            "token": str(refresh.access_token),
                            "refresh": str(refresh),
                            "created": False
                        } , status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "کاربر یافت نشد"} , status=status.HTTP_404_NOT_FOUND)
                    
                except Exception as e:
                    return Response({"message": "کاربر یافت نشد"} , status=status.HTTP_404_NOT_FOUND)
                        
            else:
                return Response(data={"message": "کد تایید ارسال شده معتبر نمیباشد و یا منقضی شده !"} , status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "خطای اعتبار سنجی پارامتر های ارسالی!"} , status=status.HTTP_400_BAD_REQUEST)

    


class UserRegisterView(APIView):
    def post(self , request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            existUser = User.objects.filter(phone_number=request.data.get("phone_number")).exists()
            if not existUser:
                serializer.save()
                return Response({"message": "ثبت نام شما در پت فیلم انجام شد. وارد شوید."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "قبلا با این شماره همراه ثبت نام کرده اید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "خطای اعتبار سنجی اطلاعات!"} , status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # دریافت Refresh Token کاربر
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # اضافه کردن توکن به لیست سیاه
            token.blacklist()

            return Response({"message": "با موفقیت از حساب خود خارج شدید."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": "خطایی رخ داد!"}, status=status.HTTP_400_BAD_REQUEST)

    
class CurrentUserView(APIView):         
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        if not user:
            return Response({"detail": "کاربر یافت نشد", "code": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)