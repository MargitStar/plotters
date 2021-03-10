from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError

from .models import Plotter, User
from .serializers import PlotterSerializer


class PlotterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        snippets = Plotter.objects.filter().all()
        serializer = PlotterSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        user = request.POST.get('user')
        serializer = PlotterSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                order_saved = serializer.save()
                return Response({"success": order_saved.pk})
        except IntegrityError:
            return Response("This Plotter already exists!")
