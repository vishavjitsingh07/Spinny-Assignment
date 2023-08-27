from rest_framework import serializers
from store.models import Cube

class AdminCubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cube
        fields = ['id','length','width','height','area','volume','created_by','created_on','updated_on']

class CubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cube
        fields = ['id','length','width','height','area','volume','updated_on']