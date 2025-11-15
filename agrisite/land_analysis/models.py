from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total area in hectares")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class LandHolder(models.Model):
    OWNERSHIP_TYPES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('government', 'Government'),
        ('community', 'Community'),
    ]
    
    name = models.CharField(max_length=200)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPES)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.ownership_type})"

class LandParcel(models.Model):
    SOIL_TYPES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silt', 'Silt'),
        ('peat', 'Peat'),
        ('chalky', 'Chalky'),
    ]
    
    land_holder = models.ForeignKey(LandHolder, on_delete=models.CASCADE, related_name='parcels')
    parcel_id = models.CharField(max_length=50, unique=True)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in hectares")
    cultivated_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in hectares")
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.parcel_id} - {self.land_holder.name}"

class IrrigationSystem(models.Model):
    SYSTEM_TYPES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler System'),
        ('flood', 'Flood Irrigation'),
        ('center_pivot', 'Center Pivot'),
        ('manual', 'Manual Irrigation'),
        ('none', 'No Irrigation'),
    ]
    
    WATER_SOURCES = [
        ('well', 'Well'),
        ('canal', 'Canal'),
        ('river', 'River'),
        ('rain', 'Rainwater'),
        ('reservoir', 'Reservoir'),
        ('municipal', 'Municipal Water'),
    ]
    
    land_parcel = models.OneToOneField(LandParcel, on_delete=models.CASCADE, related_name='irrigation')
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES)
    water_source = models.CharField(max_length=20, choices=WATER_SOURCES)
    efficiency_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Efficiency rating from 1-100"
    )
    annual_water_usage = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Annual water usage in cubic meters"
    )
    is_automated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_system_type_display()} - {self.land_parcel.parcel_id}"

class Crop(models.Model):
    CROP_TYPES = [
        ('cereal', 'Cereal'),
        ('pulse', 'Pulse'),
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('cash', 'Cash Crop'),
        ('fodder', 'Fodder Crop'),
    ]
    
    SEASONS = [
        ('kharif', 'Kharif (Monsoon)'),
        ('rabi', 'Rabi (Winter)'),
        ('zaid', 'Zaid (Summer)'),
        ('annual', 'Annual'),
    ]
    
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    season = models.CharField(max_length=20, choices=SEASONS)
    growth_period = models.IntegerField(help_text="Growth period in days")
    water_requirement = models.DecimalField(max_digits=6, decimal_places=2, help_text="Water requirement in mm")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_season_display()})"

class CroppingPattern(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='cropping_patterns')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    year = models.IntegerField()
    season = models.CharField(max_length=20, choices=Crop.SEASONS)
    area_allocated = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in hectares")
    yield_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Yield in tons")
    revenue = models.DecimalField(max_digits=12, decimal_places=2, help_text="Revenue in local currency")
    
    class Meta:
        unique_together = ['land_parcel', 'crop', 'year', 'season']
        ordering = ['-year', 'season']
    
    def __str__(self):
        return f"{self.crop.name} - {self.land_parcel.parcel_id} ({self.year})"

class LandAnalysis(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='analyses')
    analysis_date = models.DateField(auto_now_add=True)
    soil_health_index = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    water_availability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Water availability percentage"
    )
    productivity_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    recommendations = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-analysis_date']
        verbose_name_plural = "Land Analyses"
    
    def __str__(self):
        return f"Analysis for {self.land_parcel.parcel_id} - {self.analysis_date}"