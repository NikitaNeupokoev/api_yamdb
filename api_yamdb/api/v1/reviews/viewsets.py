from rest_framework import mixins, viewsets

from api.v1.mixins import PatchModelMixin


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для операций создания, получения списка
    и удаления объектов.
    """


class ViewSetWithoutUpdate(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    PatchModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet для операций создания, получения
    частичного обновления, удаления и
    получения списка объектов.
    """
