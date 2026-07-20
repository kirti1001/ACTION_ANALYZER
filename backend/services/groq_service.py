import requests
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class GroqService:
    """
    Service to interact with Groq API securely from backend.
    API key is stored server-side and NEVER exposed to frontend.
    """
    
    BASE_URL = 'https://api.groq.com/openai/v1/chat/completions'
    MODEL = 'llama-3.3-70b-versatile'
    
    def __init__(self, api_key: str):
        """Initialize with API key from environment (backend only)"""
        if not api_key:
            raise ValueError('GROQ_API_KEY not configured')
        self.api_key = api_key
    
    def generate_movement_report(self, metadata: Dict, frames: List) -> str:
        """
        Generate comprehensive movement analysis report using Groq LLM.
        
        Args:
            metadata: Analysis metadata (timestamp, duration, totalFrames)
            frames: List of frame data with landmarks and features
        
        Returns:
            str: Generated analysis report
        """
        try:
            # Build the prompt with analysis data
            prompt = self._build_prompt(metadata, frames)
            
            # Call Groq API
            response = self._call_groq_api(prompt)
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Groq API request failed: {str(e)}")
            raise Exception(f"API call failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _build_prompt(self, metadata: Dict, frames: List) -> str:
        """
        Build the prompt for Groq API.
        """
        frame_summary = json.dumps(frames[:5], indent=2) if frames else "No frames available"
        
        prompt = f"""You are an expert in human movement analysis and biomechanics.
Analyze the following pose detection data from a user's physical activity session (collected via MediaPipe Pose landmarks).

Data Summary:
- Duration: {metadata.get('duration', 'unknown')} seconds
- Total Frames: {metadata.get('totalFrames', 0)}
- Timestamp: {metadata.get('timestamp', 'unknown')}

Sample Frame Structure (showing landmarks and features for {len(frames)} frames):
{frame_summary}

Key Features:
- Landmarks: 33 body points (nose, shoulders, hips, knees) with x,y,z coordinates and visibility scores.
- Extracted Metrics: shoulder_pitch (degrees), torso_tilt (degrees), joint_velocity (px/s), step_symmetry (difference), quality_score (% visible landmarks).

Generate a comprehensive, professional movement report for the user. Structure it as follows:
1. **Summary**: Overview of session
2. **Key Metrics**: Break down averages for posture, balance, symmetry, motion
3. **Insights**: Analyze patterns and biomechanical observations
4. **Recommendations**: Personalized tips and risk flags
5. **Overall Score**: 0-100% efficiency rating

Make it engaging, actionable. Use bullet points/tables for readability. Base analysis strictly on data—be positive and encouraging."""
        
        return prompt
    
    def _call_groq_api(self, prompt: str) -> str:
        """
        Make authenticated request to Groq API.
        API key is used server-side only - never sent to client.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': self.MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1024,
            'top_p': 1,
            'stream': False
        }
        
        try:
            response = requests.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Check for errors
            if response.status_code != 200:
                error_msg = response.text
                logger.error(f"Groq API error: {response.status_code} - {error_msg}")
                raise Exception(f"API returned status {response.status_code}")
            
            data = response.json()
            
            # Extract message content
            if 'choices' not in data or not data['choices']:
                raise Exception("Invalid API response format")
            
            content = data['choices'][0]['message']['content']
            logger.info("Successfully generated report via Groq API")
            
            return content
            
        except requests.Timeout:
            raise Exception("API request timeout")
        except Exception as e:
            logger.error(f"API call error: {str(e)}")
            raise
