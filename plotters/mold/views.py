from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Mold
from .serializers import MoldSerializer


class MoldView(APIView):
    permission_classes = (IsAuthenticated,)

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

    def get(self, request, pk, format=None):
        mold = self.get_object(pk)
        try:
            serializer = MoldSerializer(mold)
            return Response(serializer.data)
        except mold.DoesNotExist:
            raise Http404
