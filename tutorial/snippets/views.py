# from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet, User
from .permissions import IsOwnerOrReadonly
from .serializers import SnippetSerializer, UserSerializer, RegistrationSerializer


@api_view(['GET', 'POST'])
def registration_view(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = RegistrationSerializer(user, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'snippets': reverse('snippet-list', request=request)
    })


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
