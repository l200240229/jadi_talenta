from rest_framework import serializers
from .models import Profile
from skills.serializers import SkillSerializer
from experiences.serializers import ExperienceSerializer
import re

class PublicProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username")
    foto = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "nama",
            "prodi",
            "angkatan",
            "bio",
            "foto",
            "kontak_email",
            "kontak_wa",
            "instagram",
            "skills",
            "experiences",
        ]

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    foto = serializers.ImageField(use_url=True)

    def validate_kontak_wa(self, value):
        if not value:
            return value

        value = re.sub(r"\s+", "", value)

        if value.startswith("08"):
            value = "62" + value[1:]

        if not re.fullmatch(r"62\d{9,13}", value):
            raise serializers.ValidationError(
                "Nomor WhatsApp harus diawali 62 dan valid."
            )

        return value

    def validate_instagram(self, value):
        if value and ("@" in value or " " in value):
            raise serializers.ValidationError(
                "Username Instagram tidak boleh mengandung @ atau spasi."
            )
        return value


    class Meta:
        model = Profile
        fields = [
            "id", "user", "nama", "prodi", "angkatan",
            "bio", "foto","kontak_email","kontak_wa", "instagram", "linkedin", "is_active"
        ]
        read_only_fields = ["user", "is_active"]

    def validate_angkatan(self, value):
        if value == "":
            return value
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("Angkatan harus 4 digit.")
        return value


    def validate_nama(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Nama minimal 3 huruf.")
        return value