from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import logging
from backend.services.groq_service import GroqService
from backend.utils.validators import validate_analysis_request
from backend.utils.rate_limit import rate_limit

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/v1/analysis')
logger = logging.getLogger(__name__)

def check_api_key(f):
    """Validate API key in Authorization header"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        return f(*args, **kwargs)
    return decorated_function

@analysis_bp.route('/generate-report', methods=['POST'])
@rate_limit(limit=100, window=3600)  # 100 requests per hour
@check_api_key
def generate_report():
    """
    Generate AI analysis report from pose data
    
    Expected JSON:
    {
        "metadata": {
            "timestamp": "ISO timestamp",
            "duration": 5,
            "totalFrames": 10
        },
        "frames": [...frame data...]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate analysis data
        is_valid, error_msg = validate_analysis_request(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Extract data
        metadata = data.get('metadata', {})
        frames = data.get('frames', [])
        
        logger.info(f"Processing analysis for {len(frames)} frames")
        
        # Call Groq API via service (API key never exposed to frontend)
        groq_service = GroqService(current_app.config['GROQ_API_KEY'])
        report = groq_service.generate_movement_report(metadata, frames)
        
        return jsonify({
            'success': True,
            'report': report,
            'timestamp': metadata.get('timestamp'),
            'frameCount': len(frames)
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate report. Please try again.'
        }), 500

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'analysis-api'
    }), 200

@analysis_bp.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded. Maximum 100 requests per hour.',
        'retry_after': 3600
    }), 429
