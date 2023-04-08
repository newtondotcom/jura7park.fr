from rest_framework import routers, serializers, viewsets
from points.views import PointsViewSet

router = routers.DefaultRouter()
router.register('points', PointsViewSet)