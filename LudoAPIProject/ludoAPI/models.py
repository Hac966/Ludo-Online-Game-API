import secrets
import string
from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Sessions(models.Model):
    # Ensure unique=True so URLs never conflict
    name = models.CharField(max_length=20, unique=True, blank=True)

    player1 = models.CharField(max_length=100, null=True, blank=True, default=None)
    player2 = models.CharField(max_length=100, null=True, blank=True, default=None)
    player3 = models.CharField(max_length=100, null=True, blank=True, default=None)
    player4 = models.CharField(max_length=100, null=True, blank=True, default=None)

    player1MovedPiece = models.CharField(max_length=2, null=True, blank=True, default=None)
    player2MovedPiece = models.CharField(max_length=2, null=True, blank=True, default=None)
    player3MovedPiece = models.CharField(max_length=2, null=True, blank=True, default=None)
    player4MovedPiece = models.CharField(max_length=2, null=True, blank=True, default=None)

    player1DieNumber = models.IntegerField(default=0)
    player2DieNumber = models.IntegerField(default=0)
    player3DieNumber = models.IntegerField(default=0)
    player4DieNumber = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.name:
            # Generates a 20-character random string (letters and numbers)
            alphabet = string.ascii_letters + string.digits
            while True:
                new_name = ''.join(secrets.choice(alphabet) for _ in range(20))
                # Check if this name already exists in the DB
                if not Sessions.objects.filter(name=new_name).exists():
                    self.name = new_name
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name