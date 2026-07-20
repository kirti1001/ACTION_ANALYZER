// ============================================
// SECURE VERSION - NO API KEYS IN FRONTEND
// ============================================
// This version calls a secure backend endpoint
// API keys are managed server-side only
// ============================================

const DEBUG = false; // Disabled in production
const BACKEND_URL = 'http://localhost:5000/api/v1/analysis'; // Secure backend endpoint

function log(...args) {
  if (DEBUG) console.log('[AI Analyzer]', ...args);
}

function error(...args) {
  console.error('[AI Analyzer]', ...args);
}

// Constants
const FPS_CAP = 20;
const SAMPLING_FPS = 2;
const VISIBLE_THRESHOLD = 0.4;
const ANALYSIS_MAX_SAMPLES = 100;
const CONNECTIONS = [
  [11,12],[11,13],[13,15],[12,14],[14,16],
  [23,24],[23,25],[25,27],[24,26],[26,28],
  [0,23],[0,24],[11,23],[11,12],[12,24]
];
let currentReport = null;

// Throttle for efficiency
function throttle(fn, limit) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      return fn(...args);
    }
  };
}

// Batch DOM updates with RAF
let rafId = null;
function batchUpdate(fn) {
  if (rafId) cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(() => {
    fn();
    rafId = null;
  });
}

// Metrics calculation
function calculateMetrics(landmarks, previous) {
  if (!landmarks || landmarks.length < 1) return { posture: 0, balance: 0, symmetry: 0, motion: 0 };

  const leftShoulder = landmarks[11], rightShoulder = landmarks[12];
  const leftHip = landmarks[23], rightHip = landmarks[24];
  const leftKnee = landmarks[25], rightKnee = landmarks[26];

  const shoulderVec = { x: rightShoulder.x - leftShoulder.x, y: rightShoulder.y - leftShoulder.y };
  const hipVec = { x: rightHip.x - leftHip.x, y: rightHip.y - leftHip.y };
  const magS = Math.hypot(shoulderVec.x, shoulderVec.y);
  const magH = Math.hypot(hipVec.x, hipVec.y);
  let postureAngle = 0;
  if (magS > 0 && magH > 0) {
    const dot = shoulderVec.x * hipVec.x + shoulderVec.y * hipVec.y;
    postureAngle = Math.acos(Math.max(-1, Math.min(1, dot / (magS * magH)))) * 180 / Math.PI;
  }
  const postureScore = Math.max(0, 100 - Math.abs(postureAngle - 180));

  const hipDiff = Math.abs(leftHip.y - rightHip.y);
  const kneeDiff = Math.abs(leftKnee.y - rightKnee.y);
  const balanceScore = Math.max(0, 100 - (hipDiff + kneeDiff) * 1000);

  const leftArm = Math.hypot(leftShoulder.x - landmarks[13].x, leftShoulder.y - landmarks[13].y);
  const rightArm = Math.hypot(rightShoulder.x - landmarks[14].x, rightShoulder.y - landmarks[14].y);
  const leftLeg = Math.hypot(leftHip.x - leftKnee.x, leftHip.y - leftKnee.y);
  const rightLeg = Math.hypot(rightHip.x - rightKnee.x, rightHip.y - rightKnee.y);
  const symDiff = Math.abs(leftArm - rightArm) + Math.abs(leftLeg - rightLeg);
  const symmetryScore = Math.max(0, 100 - symDiff * 500);

  let motionScore = 100;
  if (previous) {
    const vel = Math.hypot(
      leftShoulder.x - previous[11].x, leftShoulder.y - previous[11].y,
      rightShoulder.x - previous[12].x, rightShoulder.y - previous[12].y
    ) * FPS_CAP;
    const variance = Math.abs(vel - (window.lastVel || 0));
    motionScore = Math.max(0, 100 - variance * 10);
    window.lastVel = vel;
  }

  return { posture: postureScore, balance: balanceScore, symmetry: symmetryScore, motion: motionScore };
}

// Call secure backend API (NO API KEY EXPOSED)
async function callSecureBackendAPI(analysisData) {
  const url = `${BACKEND_URL}/generate-report`;
  
  const requestBody = {
    metadata: analysisData.metadata,
    frames: analysisData.frames
  };
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer client-token' // Can be empty or minimal
      },
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Backend API error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Unknown error from backend');
    }
    
    return data.report;
    
  } catch (error) {
    console.error('Backend API call failed:', error);
    throw error;
  }
}

// Sample frame data
function sampleFrame(second, frameIndex, landmarks, frameData) {
  if (frameData.length >= ANALYSIS_MAX_SAMPLES) return;

  const landmarkNames = [
    'nose','left_eye_inner','left_eye','left_eye_outer','right_eye_inner','right_eye','right_eye_outer',
    'left_ear','right_ear','mouth_left','mouth_right','left_shoulder','right_shoulder','left_elbow',
    'right_elbow','left_wrist','right_wrist','left_pinky','right_pinky','left_index','right_index',
    'left_thumb','right_thumb','left_hip','right_hip','left_knee','right_knee','left_ankle',
    'right_ankle','left_heel','right_heel','left_foot_index','right_foot_index'
  ];

  const visibleLandmarks = {};
  landmarks.forEach((lm, i) => {
    if (lm.visibility > VISIBLE_THRESHOLD) {
      visibleLandmarks[landmarkNames[i]] = { x: lm.x, y: lm.y, z: lm.z || 0, visibility: lm.visibility };
    }
  });

  frameData.push({
    second,
    frameIndex,
    landmarks: visibleLandmarks
  });
}

// Finalize analysis and call backend
async function finalizeAnalysis(frameData, analysisData) {
  try {
    log('Analysis complete. Calling secure backend API...');
    
    // Call backend API (API key handled server-side)
    const report = await callSecureBackendAPI(analysisData);
    
    currentReport = report;
    log('Report generated successfully from backend');
    
    return report;
    
  } catch (err) {
    console.error('Backend API failed:', err);
    log('Falling back to local report generation');
    
    // Fallback: Generate local report (no API call)
    return generateLocalReport(frameData);
  }
}

// Fallback local report
function generateLocalReport(frameData) {
  const reportContent = `AI Critical Action Analyzer Report
================================================================================

📊 Analysis Summary
-------------------
- Total Frames Analyzed: ${frameData.length}
- Note: This is a local fallback report (backend API unavailable)

🎯 Key Performance Metrics
--------------------------
Analysis data collected successfully. For AI-powered insights, ensure backend is running.

📝 Technical Notes
------------------
- Data collected via MediaPipe Pose (33 landmarks, visibility >0.4)
- Sampling: 2 frames/second
- Full dataset available for backend processing

Generated by AI Critical Action Analyzer | Stay Active & Balanced! 🚀
================================================================================`;
  
  return reportContent;
}

// Initialize app (example structure)
document.addEventListener('DOMContentLoaded', () => {
  log('Secure frontend loaded - API keys kept on backend only');
  // Rest of initialization...
});
