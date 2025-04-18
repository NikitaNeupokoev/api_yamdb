from rest_framework import viewsets, mixins


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Базовый ViewSet для операций "list", "create" и "destroy".
    """
    pass
