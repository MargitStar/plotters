from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Plotter
from .serializers import PlotterSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class PlotterView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='Get Plotters', responses={200: PlotterSerializer()})
    def get(self, request):
        user = self.request.user
        if user.groups.filter(name='Dealer').exists() or user.is_superuser:
            snippets = Plotter.objects.filter().all()
            serializer = PlotterSerializer(snippets, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            if not user.is_anonymous:
                snippets = Plotter.objects.filter(user=user.pk).all()
                serializer = PlotterSerializer(snippets, many=True, context={'request': request})
                return Response(serializer.data)

    serial_number = openapi.Parameter('serial_number', openapi.IN_QUERY, description="serial_number",
                                      type=openapi.TYPE_STRING)
    user = openapi.Parameter('user', openapi.IN_QUERY, description="user",
                             type=openapi.TYPE_INTEGER)
    ip = openapi.Parameter('ip', openapi.IN_QUERY, description="ip", type=openapi.TYPE_STRING)

    @swagger_auto_schema(operation_description='Post Plotter', responses={200: PlotterSerializer()},
                         manual_parameters=[serial_number, user, ip])
    def post(self, request):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Dealer').exists():
            serializer = PlotterSerializer(data=request.data)
        else:
            return Response("User has no permission")
        try:
            if serializer.is_valid(raise_exception=True):
                order_saved = serializer.save()
                return Response({"success": order_saved.pk})
        except IntegrityError:
            return Response("This Plotter already exists!")


class PlotterDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Plotter.objects.get(pk=pk)
        except Plotter.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Get particular Plotter', responses={200: PlotterSerializer()})
    def get(self, request, pk, format=None):
        user = self.request.user
        plotter = self.get_object(pk)
        if user.groups.filter(name='Dealer').exists() or user.is_superuser:
            serializer = PlotterSerializer(plotter)
        else:
            for user_ in plotter.user.all():
                if user_ == user:
                    plotter = self.get_object(pk)
                    serializer = PlotterSerializer(plotter)
                else:
                    return Response("User has no permission")

        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Put particular Plotter', responses={200: PlotterSerializer()})
    def put(self, request, pk, format=None):
        user = self.request.user
        plotter = self.get_object(pk)
        try:
            if user.groups.filter(name='Dealer').exists() or user.is_superuser:
                serializer = PlotterSerializer(plotter, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        except IntegrityError:
            return Response('This plotter already exists')

        return Response("User has no permission")

    @swagger_auto_schema(operation_description='Delete particular Plotter', responses={200: PlotterSerializer()})
    def delete(self, request, pk, format=None):
        user = self.request.user
        if user.is_superuser:
            plotter = self.get_object(pk)
            plotter.delete()
            return Response("Plotter was deleted successfully", status=status.HTTP_204_NO_CONTENT)
        return Response('There is no such an item')
