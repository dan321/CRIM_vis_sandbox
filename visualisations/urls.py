from django.urls import path
from . import views

urlpatterns = [
path('<slug:slug>/observations-heatmap/', views.PieceObservationsView.as_view(), name='observations-heatmap'),
path('<slug:slug>/relationships-heatmap/', views.PieceRelationshipsView.as_view(), name='relationships-heatmap'),
path('<slug:slug>/observations/', views.observation_json_view, name='json-observations'),
path('<slug:slug>/relationships/', views.relationship_json_view, name='json-relationships'),
path('<slug:slug>/auto/', views.auto_heatmap_json, name='json-auto-observations'),
path('<slug:slug>/', views.PieceDetailView.as_view(), name='piece-detail'),
path('', views.PieceListView.as_view(), name='piece-list'),
path('network-data', views.network_data_view, name='network-data')
]