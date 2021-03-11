from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Plotter
from .serializers import PlotterSerializer


class PlotterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        if user.groups.filter(name='Dealer').exists() or user.is_superuser:
            snippets = Plotter.objects.filter().all()
            serializer = PlotterSerializer(snippets, many=True, context={'request': request})
        else:
            if not user.is_anonymous:
                snippets = Plotter.objects.filter(user=user.pk).all()
                serializer = PlotterSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PlotterSerializer(data=request.data)
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

    def put(self, request, pk, format=None):
        user = self.request.user
        plotter = self.get_object(pk)
        if user.groups.filter(name='Dealer').exists() or user.is_superuser:
            serializer = PlotterSerializer(plotter, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        return Response("User has no permission")

    def delete(self, request, pk, format=None):
        user = self.request.user
        if user.is_superuser:
            plotter = self.get_object(pk)
            plotter.delete()
            return Response("Plotter was deleted successfully", status=status.HTTP_204_NO_CONTENT)
        return Response('There is no such an item')
