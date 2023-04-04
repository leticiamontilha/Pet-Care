from rest_framework import serializers

class GroupSerializer(serializers.Serializer):
    scientific_name = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
