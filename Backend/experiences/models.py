from django.db import models
from profiles.models import Profile

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()

    TIPE_CHOICES = [
        ("organisasi", "Organisasi"),
        ("lomba", "Lomba"),
        ("kerja", "Kerja"),
    ]

    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    tahun_mulai = models.IntegerField()
