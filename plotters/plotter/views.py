
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group

from .models import Plotter
from .serializers import PlotterSerializer


class PlotterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        print(user)
        if user.groups.filter(name='Dealer').exists() or user.is_superuser:
            snippets = Plotter.objects.filter().all()
            serializer = PlotterSerializer(snippets, many=True, context={'request': request})
        else:
            snippets = Plotter.objects.filter(user=user.pk).all()
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
