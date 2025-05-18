from rest_framework import serializers

class SimilarityResultSerializer(serializers.Serializer):
    input_image = serializers.URLField()
    similar_image = serializers.URLField()
    similarity = serializers.FloatField()
