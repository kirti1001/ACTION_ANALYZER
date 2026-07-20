from typing import Tuple

def validate_analysis_request(data: dict) -> Tuple[bool, str]:
    """
    Validate incoming analysis request data.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body cannot be empty"
    
    # Check metadata
    metadata = data.get('metadata')
    if not metadata:
        return False, "Missing metadata field"
    
    if not isinstance(metadata, dict):
        return False, "Metadata must be an object"
    
    # Validate metadata fields
    if 'timestamp' not in metadata:
        return False, "Missing timestamp in metadata"
    
    if 'duration' not in metadata:
        return False, "Missing duration in metadata"
    
    if not isinstance(metadata.get('duration'), (int, float)) or metadata['duration'] <= 0:
        return False, "Duration must be a positive number"
    
    # Check frames
    frames = data.get('frames')
    if frames is None:
        return False, "Missing frames field"
    
    if not isinstance(frames, list):
        return False, "Frames must be an array"
    
    if len(frames) == 0:
        return False, "Frames array cannot be empty"
    
    if len(frames) > 1000:
        return False, "Maximum 1000 frames allowed"
    
    # Validate each frame
    for i, frame in enumerate(frames):
        if not isinstance(frame, dict):
            return False, f"Frame {i} is not an object"
        
        if 'landmarks' not in frame:
            return False, f"Frame {i} missing landmarks"
    
    return True, ""
