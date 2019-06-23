from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, ListView
from visualisations.models import Piece
import requests
from dal import autocomplete


# Create your views here.
def relationship_json_view(request, slug):
    json =  requests.get(f"https://crimproject.org/pieces/{slug}/relationships/?format=json").json()

    return JsonResponse(json)

def observation_json_view(request, slug):
    json =  requests.get(f"https://crimproject.org/pieces/{slug}/observations/?format=json").json()

    return JsonResponse(json)



class PieceDetailView(DetailView):
    model = Piece
    slug_field = "piece_id"



class PieceListView(ListView):
    model = Piece