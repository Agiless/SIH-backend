# api/models.py
from django.db import models

class TripPlan(models.Model):
    # Trip Details
    destination = models.CharField(max_length=100)
    numberOfPersons = models.IntegerField()
    estimatedCost = models.FloatField()

    # Preferences
    food = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Budget
    budgetType = models.CharField(max_length=50)
    budgetAmount = models.IntegerField(blank=True, null=True)

    # Contacts
    emergencyContact = models.CharField(max_length=20)
    companionContact = models.CharField(max_length=20, blank=True, null=True)

    # Metadata
    submittedAt = models.DateTimeField()

    def __str__(self):
        return f"Trip to {self.destination} for {self.numberOfPersons} person(s)"