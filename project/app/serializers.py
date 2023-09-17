from rest_framework import serializers

class UrineStripSerializer(serializers.Serializer):
    image = serializers.ImageField()
