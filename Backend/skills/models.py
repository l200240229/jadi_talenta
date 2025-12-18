from django.db import models
from profiles.models import Profile

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    nama_skill = models.CharField(max_length=100)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner'
    )

    def __str__(self):
        return f"{self.nama_skill} ({self.profile.nama})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "nama_skill"],
                name="unique_skill_per_profile"
            )
        ]