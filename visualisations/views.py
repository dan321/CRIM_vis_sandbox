from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, ListView
from visualisations.models import Piece
import requests
from dal import autocomplete
from django.templatetags.static import static
import pandas as pd


# Create your views here.
def index(request):
    return render(request, 'index.html')

def relationship_json_view(request, slug):
    json =  requests.get(f"https://crimproject.org/pieces/{slug}/relationships/?format=json").json()
    return JsonResponse(json)


def observation_json_view(request, slug):
    json =  requests.get(f"https://crimproject.org/pieces/{slug}/observations/?format=json").json()
    return JsonResponse(json)


def network_data_view(request):
    
    # Create edges

    edges_dicts = []
    edges = pd.read_csv('static/data/relationship_edges_without_duplicates.csv')
    for edge in edges.itertuples():
        edges_dicts.append(
            {
                'from': edge.Source,
                'to': edge.Target,
                'label': '' #edge.Label
            }
        )

    
    # Create nodes
    nodes = pd.read_csv('static/data/relationship_node_list.csv')

    node_dicts = []
    for node in nodes.itertuples():
        node_dicts.append(
            {
                'id': node.Id,
                'label': node.Label,
                'group': node.Group
            }
        )


    combined = {'nodes': node_dicts, 'edges': edges_dicts}

    return JsonResponse(combined)


class PieceDetailView(DetailView):
    model = Piece
    slug_field = "piece_id"



class PieceListView(ListView):
    model = Piece