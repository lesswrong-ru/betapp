from rest_framework import serializers
from restful_api.models import Bet

class BetByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('title', 'confidence')

class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('id', 'title', 'confidence')

        def getId(self):
            return id;
