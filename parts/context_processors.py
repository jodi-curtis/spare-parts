from .models import Part
from django.db.models import F

def low_stock_count(request):
    # Count the number of parts which are low in stock
    count = Part.objects.filter(num_in_stock__lte=F('low_stock_warning')).count()
    return {'low_stock_count': count}
