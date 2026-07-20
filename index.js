// ============================================
// SECURE VERSION - NO API KEYS IN FRONTEND
// ============================================
// WARNING: This version has been secured.
// All API calls are now routed through backend.
// API keys are stored securely server-side.
// ============================================

const DEBUG = false; // Disabled - use console methods directly

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
const RETRY_ATTEMPTS = 3;
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

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
  console.log('✅ AI Critical Action Analyzer loaded securely');
  console.log('🔒 API Keys: Protected (server-side)');
  console.log('📡 Mode: Backend API mode');
});
