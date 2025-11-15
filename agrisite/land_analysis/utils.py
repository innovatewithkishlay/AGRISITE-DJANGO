import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64
from django.db.models import Count, Sum, Avg
from .models import LandParcel, IrrigationSystem, CroppingPattern

def generate_land_analysis_charts():
    """Generate various charts for land analysis"""
    charts = {}
    
    try:
        # Chart 1: Land Distribution by Soil Type
        soil_data = LandParcel.objects.values('soil_type').annotate(
            count=Count('id'),
            total_area=Sum('total_area')
        )
        
        if soil_data:
            df_soil = pd.DataFrame(list(soil_data))
            if not df_soil.empty:
                plt.figure(figsize=(10, 6))
                plt.pie(df_soil['total_area'], labels=df_soil['soil_type'], autopct='%1.1f%%', startangle=90)
                plt.title('Land Distribution by Soil Type', fontsize=14, fontweight='bold')
                plt.axis('equal')
                charts['soil_distribution'] = get_chart_image()
                plt.close()

        # Chart 2: Irrigation System Distribution
        irrigation_data = IrrigationSystem.objects.values('system_type').annotate(
            count=Count('id')
        )
        
        if irrigation_data:
            df_irrigation = pd.DataFrame(list(irrigation_data))
            if not df_irrigation.empty:
                plt.figure(figsize=(12, 6))
                sns.barplot(data=df_irrigation, x='system_type', y='count', palette='viridis')
                plt.title('Irrigation System Distribution', fontsize=14, fontweight='bold')
                plt.xlabel('System Type')
                plt.ylabel('Count')
                plt.xticks(rotation=45)
                plt.tight_layout()
                charts['irrigation_distribution'] = get_chart_image()
                plt.close()

        # Chart 3: Crop Productivity
        crop_data = CroppingPattern.objects.values('crop__name').annotate(
            total_yield=Sum('yield_amount'),
            total_area=Sum('area_allocated')
        )[:10]
        
        if crop_data:
            df_crop = pd.DataFrame(list(crop_data))
            if not df_crop.empty and (df_crop['total_area'] > 0).any():
                df_crop['productivity'] = df_crop['total_yield'] / df_crop['total_area']
                
                plt.figure(figsize=(12, 6))
                sns.barplot(data=df_crop, x='crop__name', y='productivity', palette='coolwarm')
                plt.title('Crop Productivity (Yield per Hectare)', fontsize=14, fontweight='bold')
                plt.xlabel('Crop')
                plt.ylabel('Productivity (tons/hectare)')
                plt.xticks(rotation=45)
                plt.tight_layout()
                charts['crop_productivity'] = get_chart_image()
                plt.close()

        # Chart 4: Year-wise Production Trend
        trend_data = CroppingPattern.objects.values('year').annotate(
            total_yield=Sum('yield_amount')
        ).order_by('year')
        
        if trend_data:
            df_trend = pd.DataFrame(list(trend_data))
            if not df_trend.empty:
                plt.figure(figsize=(12, 6))
                plt.plot(df_trend['year'], df_trend['total_yield'], marker='o', linewidth=2, markersize=8)
                plt.title('Year-wise Production Trend', fontsize=14, fontweight='bold')
                plt.xlabel('Year')
                plt.ylabel('Total Yield (tons)')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                charts['production_trend'] = get_chart_image()
                plt.close()

        # Chart 5: Land Holding by Ownership Type
        ownership_data = LandParcel.objects.values(
            'land_holder__ownership_type'
        ).annotate(
            total_area=Sum('total_area'),
            parcel_count=Count('id')
        )
        
        if ownership_data:
            df_ownership = pd.DataFrame(list(ownership_data))
            if not df_ownership.empty:
                plt.figure(figsize=(10, 6))
                plt.pie(df_ownership['total_area'], labels=df_ownership['land_holder__ownership_type'], 
                        autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
                plt.title('Land Distribution by Ownership Type', fontsize=14, fontweight='bold')
                plt.axis('equal')
                charts['ownership_distribution'] = get_chart_image()
                plt.close()

    except Exception as e:
        # Return empty charts if there's an error
        print(f"Error generating charts: {e}")
        charts = {}

    return charts

def get_chart_image():
    """Convert matplotlib chart to base64 image"""
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic

def generate_simple_chart(data, chart_type='bar', title='Chart', xlabel='X', ylabel='Y'):
    """Generate a simple chart with given data"""
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'bar':
        plt.bar(range(len(data)), list(data.values()))
        plt.xticks(range(len(data)), list(data.keys()), rotation=45)
    elif chart_type == 'line':
        plt.plot(list(data.keys()), list(data.values()), marker='o')
    elif chart_type == 'pie':
        plt.pie(list(data.values()), labels=list(data.keys()), autopct='%1.1f%%')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    
    chart_image = get_chart_image()
    plt.close()
    
    return chart_image

def calculate_land_utilization_efficiency():
    """Calculate land utilization efficiency metrics"""
    try:
        total_land = LandParcel.objects.aggregate(Sum('total_area'))['total_area__sum'] or 0
        cultivated_land = LandParcel.objects.aggregate(Sum('cultivated_area'))['cultivated_area__sum'] or 0
        
        if total_land > 0:
            utilization_rate = (cultivated_land / total_land) * 100
        else:
            utilization_rate = 0
            
        return {
            'total_land': total_land,
            'cultivated_land': cultivated_land,
            'utilization_rate': utilization_rate,
            'uncultivated_land': total_land - cultivated_land
        }
    except Exception as e:
        return {
            'total_land': 0,
            'cultivated_land': 0,
            'utilization_rate': 0,
            'uncultivated_land': 0
        }