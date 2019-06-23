from django.urls import path
from . import views

urlpatterns = [
path('<slug:slug>/observations/', views.observation_json_view, name='json-observations'),
path('<slug:slug>/relationships/', views.relationship_json_view, name='json-relationships'),
path('<slug:slug>/', views.PieceDetailView.as_view(), name='piece-detail'),
path('', views.PieceListView.as_view(), name='piece-list'),
]