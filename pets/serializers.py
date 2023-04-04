from rest_framework import serializers
from .models import SexPets
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexPets.choices,
        default=SexPets.DEFAULT
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
