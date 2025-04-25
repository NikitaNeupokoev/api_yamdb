from rest_framework import mixins, viewsets

from .mixins import PatchModelMixin


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Базовый ViewSet для операций "list", "create" и "destroy"."""


class ViewSetWithoutUpdate(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    PatchModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для операций default "create()", "retrieve()", "partial_update()"
    "destroy()" and "list()"
    """

