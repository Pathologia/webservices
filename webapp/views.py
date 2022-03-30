from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import result
from . serializers import resultSerializer
import subprocess
import mysql.connector
from mysql.connector import Error
#from subprocess import Popen, PIPE



# Create your views here.

class resultList(APIView):
    def get(self, request):
        result1 = result.objects.all()
        serializer = resultSerializer(result1, many=True)
        return Response(serializer.data)
    def post(self):
        pass
    
class ExecutePythonFileView(APIView):
    def get(self, request):
        try:
            subprocess.check_output(['python', 'code.py'])
        except subprocess.CalledProcessError as e:
            return HttpResponse("Failed!")
            
        return HttpResponse("Executed!")

class ExecuteWebDataView(APIView):
    def get(self, request):
        try:
            cnx = mysql.connector.connect(host='localhost',
                                            database='test',
                                            user='root',
                                            password='')
            cursor = cnx.cursor()

            cursor.execute("SELECT max(id), name FROM test")

            result = cursor.fetchall()

            for x in result:
                print(x)

        except mysql.connector.Error as err:
            return HttpResponse("Failed!")
            
        return HttpResponse("Executed!")

        




    
        
