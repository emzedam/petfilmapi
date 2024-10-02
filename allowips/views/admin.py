from django.shortcuts import render
from rest_framework import viewsets
from allowips.serializers import AllowedIPSerializer
from allowips.permissions import IsAuthenticated
from allowips.models import AlloweIps
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class AllowedApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AlloweIps.objects.all()
    serializer_class = AllowedIPSerializer

