import logging

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from trainer.models import Trainer

from .serializers import TrainerSerializer


log = logging.getLogger(__name__)


class TrainerViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'list']
    queryset = Trainer.objects.order_by('id')
    serializer_class = TrainerSerializer
    lookup_field = 'user__username'
