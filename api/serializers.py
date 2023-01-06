from rest_framework import serializers
from .models import *


class CandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidates
        fields = ('candidate_name', 'faculty', 'goals')


class VotingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votings
        fields = '__all__'
