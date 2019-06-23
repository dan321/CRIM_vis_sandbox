from django.db import models

# Create your models here.
class Piece(models.Model):
    piece_id = models.CharField(max_length=255, unique=True, blank=False, null=False)

    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.piece_id