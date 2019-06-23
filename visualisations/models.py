from django.db import models
from django.urls import reverse 


# Create your models here.
class Piece(models.Model):
    piece_id = models.SlugField(max_length=255, unique=True, blank=False, null=False)

    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.piece_id

    
    def get_absolute_url(self):
        return reverse('piece-detail', kwargs={'slug': self.piece_id})