"""
ML Service - Integration with Member 1's AI/ML models
"""
import sys
import os

# Add ml directory to path
ml_path = os.path.join(os.path.dirname(__file__), '../../..', 'ml')
sys.path.insert(0, ml_path)

try:
    # Import Member 1's models
    from risk_prediction import predict_risk_score
    from vulnerability_model import calculate_vulnerability
    ML_MODELS_AVAILABLE = True
except ImportError:
    print("⚠️  ML models not found - using fallback calculations")
    ML_MODELS_AVAILABLE = False

class MLService:
    """Service to integrate ML models with backend"""
    
    @staticmethod
    def calculate_hazard_risk(hazard_data):
        """Calculate risk score using ML model or fallback"""
        if ML_MODELS_AVAILABLE:
            try:
                # Use Member 1's ML model
                risk_score = predict_risk_score(
                    rainfall=hazard_data.get('rainfall', 0),
                    river_level=hazard_data.get('river_level', 0),
                    elevation=hazard_data.get('elevation', 50),
                    historical_risk=hazard_data.get('historical_risk', 0),
                    drainage_quality=hazard_data.get('drainage_quality', 50)
                )
                return risk_score
            except Exception as e:
                print(f"ML model error: {e}, using fallback")
                return MLService._fallback_risk_calculation(hazard_data)
        else:
            return MLService._fallback_risk_calculation(hazard_data)
    
    @staticmethod
    def _fallback_risk_calculation(hazard_data):
        """Fallback risk calculation if ML model unavailable"""
        score = (
            0.25 * min(hazard_data.get('rainfall', 0) / 100, 1.0) * 100 +
            0.25 * min(hazard_data.get('river_level', 0) / 10, 1.0) * 100 +
            0.15 * (100 - min(hazard_data.get('elevation', 50), 100)) +
            0.15 * hazard_data.get('historical_risk', 0) +
            0.10 * (100 - hazard_data.get('drainage_quality', 50)) +
            0.10 * (20 if hazard_data.get('forecast_trend') == "increasing" else 0)
        )
        return min(score, 100.0)
    
    @staticmethod
    def calculate_household_vulnerability(household_data):
        """Calculate vulnerability using ML model or fallback"""
        if ML_MODELS_AVAILABLE:
            try:
                # Use Member 1's ML model
                vulnerability_score = calculate_vulnerability(
                    children=household_data.get('children', 0),
                    elderly=household_data.get('elderly', 0),
                    disabled=household_data.get('disabled', 0),
                    medical_dependency=household_data.get('medical_dependency', False),
                    building_condition=household_data.get('building_condition', 'good')
                )
                return vulnerability_score
            except Exception as e:
                print(f"ML model error: {e}, using fallback")
                return MLService._fallback_vulnerability_calculation(household_data)
        else:
            return MLService._fallback_vulnerability_calculation(household_data)
    
    @staticmethod
    def _fallback_vulnerability_calculation(household_data):
        """Fallback vulnerability calculation"""
        score = 0
        
        if household_data.get('elderly', 0) > 0:
            score += 25
        if household_data.get('children', 0) > 0:
            score += 15
        if household_data.get('disabled', 0) > 0:
            score += 20
        if household_data.get('medical_dependency', False):
            score += 25
        
        building_condition = household_data.get('building_condition', 'good')
        if building_condition == 'poor':
            score += 15
        elif building_condition == 'moderate':
            score += 8
        
        return min(score, 100.0)