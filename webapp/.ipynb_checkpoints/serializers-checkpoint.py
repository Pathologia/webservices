from rest_framework import serializers
from . models import result

class resultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = result
         #fields=('firstname', 'lastname')
        fields = '__all__'