from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Experience
from .serializers import ExperienceSerializer
from profiles.models import Profile


class ExperienceViewSet(ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    def perform_destroy(self, instance):
        if instance.profile.user != self.request.user:
            raise PermissionDenied("Kamu tidak boleh menghapus data ini.")
        instance.delete()