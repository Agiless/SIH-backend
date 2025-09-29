# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TripPlan
from .serializers import TripPlanSerializer
import random # Used for generating sample data

class BudgetEngineView(APIView):
    """
    API view to generate and return a detailed budget for a specific trip plan.
    """

    def _generate_budget_details(self, plan):
        """
        A helper method to simulate a complex budget engine.
        This creates a large, structured dictionary with sample data.
        """
        # Use plan details to make the data feel dynamic
        base_cost = plan.estimatedCost
        persons = plan.numberOfPersons
        destination = plan.destination

        # --- Simulate complex data generation ---
        flight_cost = base_cost * 0.4
        hotel_cost = base_cost * 0.35
        activity_cost = base_cost * 0.15
        food_cost = persons * 7 * 50 # Assuming a 7-day trip at $50/day/person
        
        total_calculated_cost = flight_cost + hotel_cost + activity_cost + food_cost

        return {
            'trip_id': plan.id,
            'destination': destination,
            'summary': {
                'total_estimated_cost': round(total_calculated_cost, 2),
                'number_of_persons': persons,
                'duration_days': 7,
                'cost_per_person': round(total_calculated_cost / persons, 2),
            },
            'cost_breakdown': [
                {'category': 'Flights', 'cost': flight_cost, 'details': 'Round-trip economy tickets.'},
                {'category': 'Accommodation', 'cost': hotel_cost, 'details': f'7 nights at a 3-star hotel near {destination} center.'},
                {'category': 'Activities & Tours', 'cost': activity_cost, 'details': 'Museum passes and a guided city tour.'},
                {'category': 'Food & Dining', 'cost': food_cost, 'details': 'Estimated daily food budget.'},
            ],
            'suggested_flights': [
                {'airline': 'SkyHigh Airways', 'price': round(flight_cost * 0.95, 2), 'stops': 1, 'departure': '2025-10-10T08:00:00Z'},
                {'airline': 'JetStream Lines', 'price': round(flight_cost, 2), 'stops': 0, 'departure': '2025-10-10T09:30:00Z'},
                {'airline': 'BudgetFly', 'price': round(flight_cost * 1.1, 2), 'stops': 1, 'departure': '2025-10-10T06:45:00Z'},
            ],
            'accommodation_options': [
                {'name': 'The Grand Hotel', 'type': 'Hotel', 'rating': 4.5, 'price_per_night': round((hotel_cost / 7), 2)},
                {'name': 'Cozy Downtown B&B', 'type': 'B&B', 'rating': 4.8, 'price_per_night': round((hotel_cost / 7) * 0.8, 2)},
            ],
            'daily_plan_suggestion': [
                {'day': i+1, 'activity': f'Explore local market in {destination}', 'estimated_cost': random.randint(50, 100)} for i in range(7)
            ],
            'generated_at': plan.submittedAt.isoformat()
        }


    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to /api/plans/<id>/budget/
        """
        try:
            # Retrieve the specific trip plan using the primary key (pk) from the URL
            plan = TripPlan.objects.get(pk=pk)
        except TripPlan.DoesNotExist:
            return Response(
                {'error': 'Trip plan with this ID not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate the detailed budget data by calling our "engine"
        budget_data = self._generate_budget_details(plan)

        return Response(budget_data, status=status.HTTP_200_OK)

class TripPlanCreateView(APIView):
    """
    API view to create a new TripPlan from nested JSON.
    """
    def post(self, request, *args, **kwargs):
        data = request.data

        # Reshape the incoming nested JSON to a flat structure for our model
        try:
            flat_data = {
                'destination': data['tripDetails']['destination'],
                'numberOfPersons': data['tripDetails']['numberOfPersons'],
                'estimatedCost': data['tripDetails']['estimatedCost'],
                'food': data['preferences']['food'],
                'notes': data['preferences']['notes'],
                'budgetType': data['budget']['type'],
                'budgetAmount': data['budget'].get('amount'), # .get() handles optional fields
                'emergencyContact': data['contacts']['emergency'],
                'companionContact': data['contacts']['companion'],
                'submittedAt': data['submittedAt']
            }
        except KeyError as e:
            return Response(
                {'error': f'Missing key in payload: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TripPlanSerializer(data=flat_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripPlanListView(APIView):
    """
    API view to retrieve all stored TripPlans.
    """
    def get(self, request, *args, **kwargs):
        plans = TripPlan.objects.all()
        serializer = TripPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)