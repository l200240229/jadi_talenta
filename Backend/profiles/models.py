from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100, blank=True)
    angkatan = models.CharField(max_length=4, blank=True)
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to='foto/', blank=True, null=True)
    kontak_email = models.EmailField(blank=True)
    kontak_wa = models.CharField(max_length=20, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama