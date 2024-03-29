# it is made to read complex data
from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    poste = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


# vote serializer
class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ["id"]


# image serializer
