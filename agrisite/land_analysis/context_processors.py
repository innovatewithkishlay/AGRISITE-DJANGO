from django.db.models import Sum, Count, Avg
from .models import LandHolder, LandParcel, CroppingPattern

def global_stats(request):
    """Add global statistics to all templates"""
    try:
        stats = {
            'total_land_holders': LandHolder.objects.count(),
            'total_parcels': LandParcel.objects.count(),
            'total_cultivated_area': LandParcel.objects.aggregate(
                Sum('cultivated_area')
            )['cultivated_area__sum'] or 0,
            'total_crops_planted': CroppingPattern.objects.count(),
        }
    except:
        stats = {
            'total_land_holders': 0,
            'total_parcels': 0,
            'total_cultivated_area': 0,
            'total_crops_planted': 0,
        }
    
    return {
        'global_stats': stats,
        'app_name': 'AgriSite',
    }