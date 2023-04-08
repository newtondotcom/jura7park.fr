from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from points.models import points
from points.serializers import PointsSerializer

from django.db.models import IntegerField, Value

# Create your views here.
class PointsViewSet(viewsets.ModelViewSet):
    queryset = points.objects.all().order_by('-point').annotate(rank=Value(0, IntegerField()))

    serializer_class = PointsSerializer
    #permission_classes=[IsAuthenticated]