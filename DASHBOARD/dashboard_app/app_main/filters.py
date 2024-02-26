import django_filters
from .models import Spendings



class SpendingsFilter(django_filters.FilterSet):
    class Meta:
        model = Spendings
        fields = ('type', 'value', 'titel', 'importance', 'detailed_description', 'date_of_spending',)




