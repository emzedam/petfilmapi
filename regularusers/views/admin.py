from django.shortcuts import render
from rest_framework import viewsets
from regularusers.models import User
# from regularusers.serializers import RegularUserSerializer 
from regularusers.permissions import IsAuthenticated
# Create your views here.

class AdminRegularUserViews(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    # serializer_class = RegularUserSerializer
