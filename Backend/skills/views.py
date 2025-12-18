from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from .models import Skill
from .serializers import SkillSerializer
from profiles.models import Profile
from django.db import IntegrityError


class SkillViewSet(ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['level']
    search_fields = ['nama_skill']

    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        try:
            serializer.save(profile=profile)
        except IntegrityError:
            raise ValidationError({
                "nama_skill": "Skill ini sudah ada."
            })