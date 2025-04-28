from rest_framework.response import Response
from django.db.models import prefetch_related_objects


class PatchModelMixin:
    """
    Обновление экземпляра модели с использованием PATCH.
    Запрещает метод PUT.
    Сохраняет функциональность prefetch_related.
    """

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.get_queryset()
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects(
                [instance],
                *queryset._prefetch_related_lookups
            )

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
