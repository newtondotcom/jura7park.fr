from rest_framework import serializers
from points.models import points

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = points
        fields = '__all__'