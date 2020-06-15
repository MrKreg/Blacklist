from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from app.pkg.common.mixins.views import ActionMixin
from app.pkg.domains.api import serializers
from app.pkg.domains.api.serializers import DomainBlockRequestSerializer
from app.pkg.domains.choices import Status
from app.pkg.domains.models import BlockedDomain, BlockRequest


class BlockedDomainsViewSet(ModelViewSet):
    queryset = BlockedDomain.objects.all()
    serializer_class = serializers.DomainSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DomainBlockRequestView(generics.CreateAPIView):
    queryset = BlockRequest.objects.all()
    serializer_class = DomainBlockRequestSerializer
    permission_classes = (permissions.AllowAny,)


class RequestReviewViewSet(ActionMixin, GenericViewSet):
    queryset = BlockRequest.objects.filter(status=Status.CREATED.value)
    serializer_class = DomainBlockRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=True, methods=['post'], serializer_class=serializers.ApproveBlockSerializer)
    def approve(self, request, *args, **kwargs):
        print('approve')
        return self.run_action()

    @action(detail=True, methods=['post'], serializer_class=serializers.RefuseBlockSerializer)
    def refuse(self, request, *args, **kwargs):
        return self.run_action()
