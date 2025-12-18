from rest_framework import serializers
from .models import Experience
import re

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ["profile"]

    def validate_judul(self, value):
        if not value.strip():
            raise serializers.ValidationError("Judul tidak boleh kosong.")
        return value

    def validate_deskripsi(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Deskripsi minimal 10 karakter.")
        return value

    def validate_tahun_mulai(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError(
                "Tahun harus berupa 4 digit angka yang valid."
            )
        
        return value
