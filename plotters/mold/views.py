from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Mold
from .serializers import MoldSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class MoldView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='Get Molds', responses={200: MoldSerializer()})
    def get(self, request):
        snippets = Mold.objects.filter().all()
        serializer = MoldSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        user = self.request.user
        if user.is_superuser:
            serializer = MoldSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    order_saved = serializer.save()
                    return Response({"success": order_saved.pk})
            except IntegrityError:
                return Response("This Mold already exists!")


class MoldDetailView(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Mold.objects.get(pk=pk)
        except Mold.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Get Particular Mold', responses={200: MoldSerializer()})
    def get(self, request, pk, format=None):
        mold = self.get_object(pk)
        try:
            serializer = MoldSerializer(mold)
            return Response(serializer.data)
        except mold.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description='Put Particular Mold', responses={200: MoldSerializer()})
    def put(self, request, pk, format=None):
        user = self.request.user
        mold = self.get_object(pk)
        if user.is_superuser:
            try:
                serializer = MoldSerializer(mold, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            except IntegrityError:
                return Response('This mold already exists')

        return Response("User has no permission")

    @swagger_auto_schema(operation_description='Put Particular Mold', responses={204: 'Mold successfully deleted'})
    def delete(self, request, pk, format=None):
        user = self.request.user
        if user.is_superuser:
            mold = self.get_object(pk)
            try:
                mold.delete()
                return Response("Mold was deleted successfully", status=status.HTTP_204_NO_CONTENT)
            except mold.DoesNotExist:
                return Response('There is no such an item')
