from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apiv1.serializers import DeviceSerializer, MeteringSerializer
from core.models import Device, Metering


class DeviceViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['get'])
    def max_consumption(self, request, pk=None):
        obj = Metering.objects.filter(
            device_id=pk
        ).order_by('-consumption').first()

        serializer = MeteringSerializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def min_consumption(self, request, pk=None):
        obj = Metering.objects.filter(
            device_id=pk
        ).order_by('consumption').first()

        serializer = MeteringSerializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def total_consumption(self, request, pk=None):
        data = Metering.objects.filter(
            device_id=pk
        ).aggregate(Sum('consumption'))

        return Response(data)

    @action(detail=True, methods=['get'])
    def avg_consumption(self, request, pk=None):
        data = Metering.objects.filter(
            device_id=pk
        ).aggregate(Avg('consumption'))

        return Response(data)


class MeteringViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Metering.objects.all().order_by('-timestamp')
    serializer_class = MeteringSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['consumption'] < 0:
            # Avoid save negative consumptions
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
