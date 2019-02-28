from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from accounts.serializers import UserTransactionSerializer


def verify_transaction_data(params):
    own_to_id = params.get('own_to_id', '')
    user_id = params.get('user_id', '')

    if not own_to_id or not User.objects.filter(pk=params.get('own_to_id', '')).exists():
        return Response(data={'error': 'Invalid own_to ID'}, status=HTTP_400_BAD_REQUEST)

    if not user_id or not User.objects.filter(pk=params.get('user_id', '')).exists():
        return Response(data={'error': 'Invalid User ID'}, status=HTTP_400_BAD_REQUEST)

    if user_id == own_to_id:
        return Response(data={'error': 'user cannot own to itself'}, status=HTTP_400_BAD_REQUEST)

    price = params.get('price', '')
    try:
        float(price)
    except ValueError:
        return Response(data={'error': 'Invalid price'}, status=HTTP_400_BAD_REQUEST)


def add_transaction_data(params):
    serializer = UserTransactionSerializer(data=params)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.validated_data, status=HTTP_201_CREATED)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


