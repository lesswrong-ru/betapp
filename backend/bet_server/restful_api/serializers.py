from rest_framework import serializers
from restful_api.models import Bet


class BetByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('title', 'confidence', 'outcome')


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('id', 'title', 'confidence', 'outcome')

        def getId(self):
            return id


class ResolveBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('outcome',)
