from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import IsAuthorPermission
from .serializers import ProblemSerializer, ReplySerializer, CommentSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # http_method_names = ['GET', 'POST', 'PUT', 'DELETE']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer













