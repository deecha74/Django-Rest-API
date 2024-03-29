from django.shortcuts import render
from .models import *
from rest_framework import generics, permissions, mixins, status
from .serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


# for vote


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs["pk"])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("Already Voted ")
        serializer.save(
            voter=self.request.user, post=Post.objects.get(pk=self.kwargs["pk"])
        )

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ValidationError("You Never Voted !")


# this is to delete post
class PostRetrivDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs["pk"], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("You are not Allowed !")


## Creating Login ##
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse


# image


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data["username"], password=data["password"]
            )
            token = Token.objects.create(user=user)
            return JSONParser({"success": "Account Created", "token": str(token)})

        except IntegrityError:
            return JsonResponse({"error": "Username already taken !"})


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )
        if user is None:
            return JsonResponse({"error": "Please Input correct Data !"}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)

            except:
                token = Token.objects.create(user=user)

            return JsonResponse({"token": str(token)}, status=200)
