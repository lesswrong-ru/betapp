from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restful_api.models import Bet
from restful_api.serializers import BetSerializer, BetByIdSerializer, ResolveBetSerializer


@api_view(['GET', 'POST'])
def bet_list(request):
    if request.method == 'GET':
        bets = Bet.objects.all()
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH'])
def bet_detail(request, pk):
    try:
        bet = Bet.objects.get(pk=pk)
    except Bet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BetByIdSerializer(bet)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ResolveBetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(bet, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
