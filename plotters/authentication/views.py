from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.http import Http404


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_user = self.request.user
        if current_user.is_superuser:
            group, created = Group.objects.get_or_create(name="Dealer")
            group.user_set.add(user)
        elif current_user.groups.filter(name='Dealer').exists():
            group, created = Group.objects.get_or_create(name="Customer")
            group.user_set.add(user)
        else:
            group, created = Group.objects.get_or_create(name="Customer")
            group.user_set.add(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserApi(APIView):

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_superuser:
            user = User.objects.filter().all()
            serializer = UserSerializer(user, many=True)
        elif current_user.groups.filter(name='Dealer').exists():
            pass
        else:
            if not current_user.is_anonymous:
                user = User.objects.filter(pk=current_user.pk).first()
                serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk).first()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        current_user = request.user
        user = self.get_object(pk)
        if current_user.groups.filter(name='Dealer').exists() or current_user.is_superuser:
            serializer = UserSerializer(user)
        else:
            if current_user == user:
                plotter = self.get_object(pk)
                serializer = UserSerializer(plotter)
            else:
                return Response("User has no permission")
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        current_user = self.request.user
        user = self.get_object(pk)
        if current_user.is_superuser and user.groups.filter(name='Dealer').exists() and user is not None:
            user.delete()
            return Response("Plotter was deleted successfully", status=status.HTTP_204_NO_CONTENT)
        return Response('There is no such user')
