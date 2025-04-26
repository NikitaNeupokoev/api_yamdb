from rest_framework.response import Response


class PatchModelMixin:
    """
    Миксин, реализующий только PATCH (partial_update),
    без поддержки PUT (update).
    """

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
