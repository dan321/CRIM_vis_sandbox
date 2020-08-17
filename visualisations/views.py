from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, ListView
from visualisations.models import Piece
import requests
from dal import autocomplete
from django.templatetags.static import static
import pandas as pd
from django.templatetags.static import static
import crim_intervals as ci
import pandas as pd

# Utility functions
def get_match_data_for_piece(piece_id, vector_size=5, min_matches=2):
    
    url = f"https://crimproject.org/mei/{piece_id}.mei"
    score = ci.ScoreBase(url)
    vectors = ci.IntervalBase(score.note_list)
    patterns = ci.into_patterns([vectors.generic_intervals], vector_size)
    exact_matches = ci.find_exact_matches(patterns, min_matches)

    match_data = []
    
    for match_series in exact_matches:
        for match in match_series.matches:
            match_dict = {
              "pattern_generating_match": match_series.pattern,
              "pattern_matched": match.pattern, 
              "piece_title": match.first_note.metadata.title, 
              "part": match.first_note.part, 
              "start_measure": match.first_note.note.measureNumber, 
              "end_measure": match.last_note.note.measureNumber, 
              "note_durations": match.durations, 
              "ema": match.ema, 
              "ema_url": match.ema_url
            }

            match_data.append(match_dict)

    return pd.DataFrame(match_data)


def get_heatmap_data_from_df(df):

    heatmap_data = []

    for name, group in df.groupby("part"):

        matches = []

        for i, row in enumerate(group.sort_values(["start_measure"]).itertuples()):

            inner_dict = {
                "label": i,
                "data": [
                    {
                        "timeRange": [row.start_measure, row.end_measure],
                        "val": str(row.pattern_matched),
                        "url": row.ema_url
                    }
                ]
            } 

            matches.append(inner_dict)


        heatmap_data.append(
            {
                "group": name,
                "data": matches
            }
        )

    return heatmap_data


# VIEWS
def index(request):
    return render(request, 'index.html')

def auto_heatmap_json(request, slug, vector_size):
    
    try:
        df = get_match_data_for_piece(slug, vector_size)
        heatmap_data = get_heatmap_data_from_df(df)

        context = {
            "heatmap_data": heatmap_data,
            "piece_id": slug
        }
    except Exception as e:
        context = {
            "heatmap_data": {},
            "piece_id": slug
        }
    return render(request, 'visualisations/auto_heatmap.html', context=context)



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