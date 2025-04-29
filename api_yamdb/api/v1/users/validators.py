from rest_framework import serializers


def validate(value):
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Имя "me" запрещено для использования.'
        )
    return value
