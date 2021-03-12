from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cutout
from datetime import datetime
from .serializers import CutoutSerializer
from rest_framework.permissions import IsAuthenticated


class CutoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.is_superuser:
            snippets = Cutout.objects.all()
            serializer = CutoutSerializer(snippets, many=True, context={'request': request})
        elif user.groups.filter(name='Dealer').exists():
            pass
        else:
            snippets = Cutout.objects.filter(user=request.user).all()
            serializer = CutoutSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

