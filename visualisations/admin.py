from django.contrib import admin
from visualisations.models import Piece

# Register your models here.
@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    pass