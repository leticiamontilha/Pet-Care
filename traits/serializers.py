from rest_framework import serializers

class TraitSerializer(serializers.Serializer):
    trait_name = serializers.CharField(
        source="name"
    )
    created_at = serializers.ReadOnlyField(read_only=True) 