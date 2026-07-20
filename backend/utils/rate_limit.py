from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

# Simple in-memory rate limiter (for production, use Redis)
rate_limit_store = {}

def rate_limit(limit=100, window=3600):
    """
    Rate limiting decorator.
    
    Args:
        limit: Maximum number of requests
        window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr or 'unknown'
            
            # Create store key
            store_key = f"{client_ip}:{request.path}"
            now = datetime.now()
            
            # Clean old entries
            if store_key in rate_limit_store:
                requests_list = rate_limit_store[store_key]
                requests_list = [ts for ts in requests_list if now - ts < timedelta(seconds=window)]
                rate_limit_store[store_key] = requests_list
            else:
                rate_limit_store[store_key] = []
            
            # Check limit
            if len(rate_limit_store[store_key]) >= limit:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'limit': limit,
                    'window': window
                }), 429
            
            # Add current request
            rate_limit_store[store_key].append(now)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
