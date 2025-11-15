from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'total_area']
    search_fields = ['name', 'code']

@admin.register(LandHolder)
class LandHolderAdmin(ImportExportModelAdmin):
    list_display = ['name', 'ownership_type', 'region', 'contact_email']
    list_filter = ['ownership_type', 'region']
    search_fields = ['name', 'contact_email']

@admin.register(LandParcel)
class LandParcelAdmin(ImportExportModelAdmin):
    list_display = ['parcel_id', 'land_holder', 'total_area', 'cultivated_area', 'soil_type']
    list_filter = ['soil_type', 'land_holder__region']
    search_fields = ['parcel_id', 'land_holder__name']

@admin.register(IrrigationSystem)
class IrrigationSystemAdmin(ImportExportModelAdmin):
    list_display = ['land_parcel', 'system_type', 'water_source', 'efficiency_rating', 'is_automated']
    list_filter = ['system_type', 'water_source', 'is_automated']

@admin.register(Crop)
class CropAdmin(ImportExportModelAdmin):
    list_display = ['name', 'crop_type', 'season', 'growth_period', 'water_requirement']
    list_filter = ['crop_type', 'season']

@admin.register(CroppingPattern)
class CroppingPatternAdmin(ImportExportModelAdmin):
    list_display = ['land_parcel', 'crop', 'year', 'season', 'area_allocated', 'yield_amount']
    list_filter = ['year', 'season', 'crop__crop_type']

@admin.register(LandAnalysis)
class LandAnalysisAdmin(ImportExportModelAdmin):
    list_display = ['land_parcel', 'analysis_date', 'soil_health_index', 'water_availability', 'productivity_score']
    list_filter = ['analysis_date']