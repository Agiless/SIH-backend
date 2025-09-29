# api/urls.py
from django.urls import path
from .views import TripPlanCreateView, TripPlanListView, BudgetEngineView

urlpatterns = [
    # Endpoint to POST (create) a new trip plan
    path('plans/create/', TripPlanCreateView.as_view(), name='plan-create'),
    
    # Endpoint to GET all trip plans
    path('plans/', TripPlanListView.as_view(), name='plan-list'),
    path('plans/<int:pk>/budget/', BudgetEngineView.as_view(), name='plan-budget-detail'),
]