from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import result
from . serializers import resultSerializer


# Create your views here.

class resultList(APIView):
    def get(self, request):
        result1 = result.objects.all()
        serializer = resultSerializer(result1, many=True)
        return Response(serializer.data)
    def post(self):
        pass