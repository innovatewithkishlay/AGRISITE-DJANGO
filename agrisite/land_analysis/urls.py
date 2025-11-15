from django.urls import path
from . import views

urlpatterns = [
    # Core Pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Land Parcel Management
    path('parcels/', views.land_parcel_list, name='land_parcel_list'),
    path('parcels/<int:pk>/', views.land_parcel_detail, name='land_parcel_detail'),
    
    # Analysis & Reports
    path('analysis/', views.analysis_reports, name='analysis_reports'),
    path('region/<int:region_id>/', views.region_analysis, name='region_analysis'),
    path('crop/<int:crop_id>/', views.crop_analysis, name='crop_analysis'),
    
    # Data Export & Download
    path('export/<str:data_type>/', views.export_data, name='export_data'),
    path('download/report/<str:report_type>/', views.download_analysis_report, name='download_report'),
    path('download/parcel/<int:pk>/', views.download_parcel_report, name='download_parcel_report'),
    
    # API Endpoints
    path('api/land-stats/', views.api_land_stats, name='api_land_stats'),
    
    # User Management
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
]

# Handler for custom error pages
handler404 = views.handler404
handler500 = views.handler500