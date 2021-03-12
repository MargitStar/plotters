from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cutout
from datetime import datetime
from .serializers import CutoutPostSerializer, CutoutGetSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError


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
