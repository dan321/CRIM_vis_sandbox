from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, ListView
from visualisations.models import Piece
import requests
from dal import autocomplete
from django.templatetags.static import static
import pandas as pd
from django.templatetags.static import static


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
    
    try:
        edges_df = pd.read_csv(static('data/relationship_edges_without_duplicates.csv'))
        nodes_df = static('data/relationship_node_list.csv')
    except Exception as e:
        edges_df = pd.read_csv('static/data/relationship_edges_without_duplicates.csv')
        nodes_df = pd.read_csv('static/data/relationship_node_list.csv')
    

    # Create edges
    edges_dicts = []
    edges = edges_df
    for edge in edges.itertuples():
        edges_dicts.append(
            {
                'from': edge.Source,
                'to': edge.Target,
                'arrows': 'to',
                'label': '', #edge.Label,
                'title': edge.Label
            }
        )

    
    # Create nodes
    nodes = nodes_df

    node_dicts = []
    for node in nodes.itertuples():
        try:
            piece = Piece.objects.get(piece_id=node.Label)
            title = f"{piece.title} ({piece.genre})"

        except Exception as e:
            title = ''

        node_dicts.append(
            {
                'id': node.Id,
                'label': node.Label,
                'group': node.Group,
                'title': title
            }
        )


    combined = {'nodes': node_dicts, 'edges': edges_dicts}

    return JsonResponse(combined)


class PieceDetailView(DetailView):
    model = Piece
    slug_field = "piece_id"


class PieceRelationshipsView(DetailView):
    model = Piece
    slug_field = "piece_id"
    template_name = "visualisations/relationships_heatmap.html"


class PieceObservationsView(DetailView):
    model = Piece
    slug_field = "piece_id"
    template_name = "visualisations/observations_heatmap.html"



class PieceListView(ListView):
    model = Piece