from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Cutout
from .serializers import CutoutPostSerializer, CutoutGetSerializer


class CutoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.is_superuser:
            snippets = Cutout.objects.all()
            serializer = CutoutGetSerializer(snippets, many=True, context={'request': request})
        elif user.groups.filter(name='Dealer').exists():
            pass
        else:
            snippets = Cutout.objects.filter(user=request.user).all()
            serializer = CutoutGetSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        try:
            if user.groups.filter(name='Customer').exists():
                try:
                    serializer = CutoutPostSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        cutout = serializer.save(user=self.request.user, created_date=datetime.now())
                        return Response({"success": cutout.pk})
                except IntegrityError:
                    return Response("This plotter or mold does not exist")
        except PermissionError:
            return Response("User has no permission")


class CutoutDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Cutout.objects.get(pk=pk)
        except Cutout.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.request.user
        mold = self.get_object(pk)
        try:
            if user.is_superuser:
                serializer = CutoutGetSerializer(mold)
            elif user.groups.filter(name="Dealer").exists():
                pass
            else:
                if user == mold.user:
                    serializer = CutoutGetSerializer(mold)
                else:
                    return Response("User has no permission")
            return Response(serializer.data)
        except mold.DoesNotExist:
            raise Http404
