from datetime import datetime, date

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404

from .models import Cutout, MoldStatistics, PlotterStatistics
from plotter.models import Plotter
from .serializers import CutoutPostSerializer, CutoutGetSerializer, MoldSerializer, MoldGetSerializer, PlotterSerializer


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
        if user.groups.filter(name='Customer').exists():
            try:
                plotter = Plotter.objects.filter(id=request.data['plotter_id']).first()
                if user in plotter.user.all():
                    serializer = CutoutPostSerializer(data=request.data)
                    mold_serializer = MoldSerializer(data=request.data)
                    plotter_serializer = PlotterSerializer(data=request.data)
                else:
                    return Response("User has no permission!")
                if serializer.is_valid(raise_exception=True) and mold_serializer.is_valid(
                        raise_exception=True) and plotter_serializer.is_valid(raise_exception=True):
                    if plotter.cutouts >= request.data['amount'] != 0:
                        cutout = serializer.save(user=self.request.user, created_date=datetime.now())
                        mold = mold_serializer.save()
                        plotter_statistics = plotter_serializer.save(ip=plotter.ip, last_cutout_date=date.today())
                        plotter.cutouts -= request.data['amount']
                        plotter.save()
                        return Response({"success": cutout.pk})
                    elif request.data['amount'] is 0:
                        return Response('Please choose another amount, not 0!')
                    else:
                        return Response(f'You can cut out only {plotter.cutouts}')
            except IntegrityError:
                return Response("This plotter or mold does not exist")
        else:
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


class MoldView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.is_superuser:
            snippets = MoldStatistics.objects.all()
            serializer = MoldGetSerializer(snippets, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response("User has no permission!")
