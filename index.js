const DEBUG = true;

function log(...args) {
  if (DEBUG) console.log('[AI Analyzer]', ...args);
}

function error(...args) {
  console.error('[AI Analyzer]', ...args);
}

// Constants
const FPS_CAP = 20; // Pose ~30 FPS
const SAMPLING_FPS = 2; // Sample 2/sec
const VISIBLE_THRESHOLD = 0.4;
const ANALYSIS_MAX_SAMPLES = 100;
const RETRY_ATTEMPTS = 3;
const CONNECTIONS = [
  [11,12],[11,13],[13,15],[12,14],[14,16],
  [23,24],[23,25],[25,27],[24,26],[26,28],
  [0,23],[0,24],[11,23],[11,12],[12,24]
];
let report = null;

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

// Metrics (main thread for simplicity/reliability)
function calculateMetrics(landmarks, previous) {
  if (!landmarks || landmarks.length < 1) return { posture: 0, balance: 0, symmetry: 0, motion: 0 };

  const leftShoulder = landmarks[11], rightShoulder = landmarks[12];
  const leftHip = landmarks[23], rightHip = landmarks[24];
  const leftKnee = landmarks[25], rightKnee = landmarks[26];

  // Posture
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

  // Balance
  const hipDiff = Math.abs(leftHip.y - rightHip.y);
  const kneeDiff = Math.abs(leftKnee.y - rightKnee.y);
  const balanceScore = Math.max(0, 100 - (hipDiff + kneeDiff) * 1000);

  // Symmetry
  const leftArm = Math.hypot(leftShoulder.x - landmarks[13].x, leftShoulder.y - landmarks[13].y);
  const rightArm = Math.hypot(rightShoulder.x - landmarks[14].x, rightShoulder.y - landmarks[14].y);
  const leftLeg = Math.hypot(leftHip.x - leftKnee.x, leftHip.y - leftKnee.y);
  const rightLeg = Math.hypot(rightHip.x - rightKnee.x, rightHip.y - rightKnee.y);
  const symDiff = Math.abs(leftArm - rightArm) + Math.abs(leftLeg - rightLeg);
  const symmetryScore = Math.max(0, 100 - symDiff * 500);

  // Motion
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

// DOM Ready
document.addEventListener('DOMContentLoaded', async () => {
  if (typeof Pose === 'undefined' || typeof Camera === 'undefined') {
    error('Required libraries not loaded');
    alert('Libraries failed to load. Refresh page.');
    return;
  }
  log('Libraries loaded');

  // Core vars
  let pose, camera, video, canvas, ctx, skeletonCanvas, skeletonCtx;
  let isAnalyzing = false, frameData = [], sampleInterval, previousLandmarks = null, latestLandmarks = [], noPoseTimer = 0;
  let fpsCounter = { frames: 0, lastTime: 0 };
  window.lastVel = 0;
  const metricThrottle = throttle(() => calculateMetrics(latestLandmarks, previousLandmarks), 100);
  const updateSkeletonThrottle = throttle((landmarks) => {
    latestLandmarks = landmarks;
    if (skeletonCtx) updateSkeleton2D(landmarks);
  }, 100 / FPS_CAP);

  // Navbar (simplified, no errors)
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');
  const mobileAuth = document.querySelector('.mobile-auth');
  const areasDropdown = document.querySelector('.areas-dropdown');
  const body = document.body;

  function toggleMobileMenu() {
    const isOpen = navLinks.classList.toggle('active');
    mobileAuth.classList.toggle('active');
    body.classList.toggle('menu-open', isOpen);
    const icon = mobileMenuBtn.querySelector('i');
    icon.classList.toggle('fa-bars', !isOpen);
    icon.classList.toggle('fa-times', isOpen);
    if (!isOpen) areasDropdown?.classList.remove('active');
  }

  mobileMenuBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMobileMenu();
  });

  document.querySelector('.areas-dropdown .nav-link')?.addEventListener('click', (e) => {
    if (window.innerWidth <= 992) {
      e.preventDefault();
      e.stopPropagation();
      areasDropdown.classList.toggle('active');
    }
  });

  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 992) {
      if (areasDropdown?.classList.contains('active') && !areasDropdown.contains(e.target)) {
        areasDropdown.classList.remove('active');
      }
      if (navLinks.classList.contains('active') && !e.target.closest('.nav-container')) {
        toggleMobileMenu();
      }
    }
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 992) setTimeout(toggleMobileMenu, 300);
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 992) {
      navLinks.classList.remove('active');
      mobileAuth.classList.remove('active');
      body.classList.remove('menu-open');
      areasDropdown?.classList.remove('active');
      mobileMenuBtn.querySelector('i').classList.add('fa-bars');
      mobileMenuBtn.querySelector('i').classList.remove('fa-times');
    }
    if (skeletonCanvas) {
      const rect = skeletonCanvas.getBoundingClientRect();
      skeletonCanvas.width = rect.width;
      skeletonCanvas.height = rect.height;
      if (skeletonCtx) {
        updateSkeleton2D(latestLandmarks);
      }
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && window.innerWidth <= 992) {
      if (areasDropdown?.classList.contains('active')) {
        areasDropdown.classList.remove('active');
      } else {
        toggleMobileMenu();
      }
    }
  });

  // Vanta (optional, no errors)
  if (window.innerWidth > 1000 && VANTA?.NET) {
    VANTA.NET({
      el: document.body,
      mouseControls: true,
      touchControls: false,
      gyroControls: false,
      minHeight: 200,
      minWidth: 300,
      scale: 1,
      scaleMobile: 0.8,
      color: 0x3f51b5,
      backgroundColor: 0x0,
      points: 20,
      maxDistance: 15,
      spacing: 12
    });
  }

  // Pose init (no errors)
  pose = new Pose({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.2/${file}`
  });
  pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.4,
    minTrackingConfidence: 0.4
  });
  pose.onResults(onPoseResults);
  log('Pose ready');

  // Skeleton init (2D canvas only - no Three.js)
  function initSkeleton() {
    const container = document.getElementById('skeleton-canvas');
    if (!container) return error('No skeleton canvas');

    skeletonCanvas = container;
    skeletonCtx = container.getContext('2d');
    
    // Set canvas size
    const rect = container.getBoundingClientRect();
    skeletonCanvas.width = rect.width;
    skeletonCanvas.height = rect.height;
    
    log('2D Skeleton canvas ready for landmarks');
    drawStaticHuman2D();
  }

  function drawStaticHuman2D() {
    if (!skeletonCtx) return;
    const w = skeletonCanvas.width, h = skeletonCanvas.height, cx = w / 2, cy = h / 2;
    
    // Clear canvas
    skeletonCtx.clearRect(0, 0, w, h);
    
    // Draw static human figure
    skeletonCtx.strokeStyle = '#00ff00';
    skeletonCtx.lineWidth = 2;
    skeletonCtx.fillStyle = '#00ff00';
    
    skeletonCtx.beginPath();
    // Head
    skeletonCtx.arc(cx, cy - 50, 20, 0, Math.PI * 2);
    // Body
    skeletonCtx.moveTo(cx, cy - 30); 
    skeletonCtx.lineTo(cx, cy + 50);
    // Arms
    skeletonCtx.moveTo(cx, cy - 10); 
    skeletonCtx.lineTo(cx - 40, cy + 10);
    skeletonCtx.moveTo(cx, cy - 10); 
    skeletonCtx.lineTo(cx + 40, cy + 10);
    // Legs
    skeletonCtx.moveTo(cx, cy + 50); 
    skeletonCtx.lineTo(cx - 30, cy + 100);
    skeletonCtx.moveTo(cx, cy + 50); 
    skeletonCtx.lineTo(cx + 30, cy + 100);
    skeletonCtx.stroke();
  }

  function updateSkeleton2D(landmarks) {
    if (!skeletonCtx || !skeletonCanvas) return;
    
    const w = skeletonCanvas.width, h = skeletonCanvas.height;
    
    // Clear canvas
    skeletonCtx.clearRect(0, 0, w, h);
    
    if (!landmarks || landmarks.length === 0) {
      drawStaticHuman2D();
      return;
    }

    // Draw connections (bones)
    skeletonCtx.strokeStyle = '#00ff00';
    skeletonCtx.lineWidth = 3;
    skeletonCtx.beginPath();
    
    CONNECTIONS.forEach(([i, j]) => {
      if (landmarks[i]?.visibility > VISIBLE_THRESHOLD && landmarks[j]?.visibility > VISIBLE_THRESHOLD) {
        const x1 = landmarks[i].x * w;
        const y1 = landmarks[i].y * h;
        const x2 = landmarks[j].x * w;
        const y2 = landmarks[j].y * h;
        
        skeletonCtx.moveTo(x1, y1);
        skeletonCtx.lineTo(x2, y2);
      }
    });
    skeletonCtx.stroke();

    // Draw landmarks (joints)
    skeletonCtx.fillStyle = '#ff0000';
    landmarks.forEach(lm => {
      if (lm.visibility > VISIBLE_THRESHOLD) {
        const x = lm.x * w;
        const y = lm.y * h;
        
        skeletonCtx.beginPath();
        skeletonCtx.arc(x, y, 4, 0, Math.PI * 2);
        skeletonCtx.fill();
      }
    });

    // Draw landmark numbers (optional - for debugging)
    if (DEBUG) {
      skeletonCtx.fillStyle = '#ffffff';
      skeletonCtx.font = '10px Arial';
      landmarks.forEach((lm, i) => {
        if (lm.visibility > VISIBLE_THRESHOLD) {
          const x = lm.x * w;
          const y = lm.y * h;
          skeletonCtx.fillText(i.toString(), x + 5, y - 5);
        }
      });
    }
  }

  // Pose results (no errors, clean feed)
  function onPoseResults(results) {
    if (!ctx || !canvas) return;
    ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);

    if (results.poseLandmarks) {
      const visibleCount = results.poseLandmarks.filter(lm => lm.visibility > VISIBLE_THRESHOLD).length;
      const avgConf = results.poseLandmarks.reduce((sum, lm) => sum + lm.visibility, 0) / 33 * 100;

      const now = performance.now();
      fpsCounter.frames++;
      if (now - fpsCounter.lastTime >= 1000) {
        fpsCounter.frames = Math.round(fpsCounter.frames * 1000 / (now - fpsCounter.lastTime));
        fpsCounter.lastTime = now;
      }

      batchUpdate(() => {
        const landmarksEl = document.getElementById('landmarks-count');
        const confEl = document.getElementById('confidence-score');
        const fpsEl = document.getElementById('frame-rate');
        if (landmarksEl) landmarksEl.textContent = visibleCount;
        if (confEl) confEl.textContent = `${avgConf.toFixed(1)}%`;
        if (fpsEl) fpsEl.textContent = `${fpsCounter.frames} FPS`;

        // Skeleton update (throttled, synced with pose)
        updateSkeletonThrottle(Array.from(results.poseLandmarks));

        // Metrics (only during analysis)
        if (isAnalyzing) {
          const metrics = calculateMetrics(results.poseLandmarks, previousLandmarks);
          updateMetricUI('posture', metrics.posture);
          updateMetricUI('balance', metrics.balance);
          updateMetricUI('symmetry', metrics.symmetry);
          updateMetricUI('motion', metrics.motion);
        }

        // Status indicators
        const overlayEl = document.getElementById('skeleton-overlay');
        const statusEl = document.querySelector('#skeleton-status');
        if (overlayEl) overlayEl.style.display = 'none';
        if (statusEl) statusEl.className = 'indicator-dot green';
      });

      noPoseTimer = 0;
      previousLandmarks = Array.from(results.poseLandmarks);
    } else {
      noPoseTimer++;
      if (noPoseTimer > 90 && isAnalyzing) { // ~3s at 30 FPS
        alert('No pose detected. Ensure you are visible and centered in frame.');
        noPoseTimer = 0;
      }
      batchUpdate(() => {
        const statusEl = document.querySelector('#skeleton-status');
        const overlayEl = document.getElementById('skeleton-overlay');
        if (statusEl) statusEl.className = 'indicator-dot red';
        if (overlayEl) overlayEl.style.display = 'block';
        updateSkeletonThrottle([]); // Clear skeleton
      });
    }
  }

  // Update Metric UI (dynamic, with trends)
  function updateMetricUI(type, score) {
    const scoreEl = document.getElementById(`${type}-score`);
    const progressEl = document.getElementById(`${type}-progress`);
    const trendEl = document.getElementById(`${type}-trend`);
    if (!scoreEl || !progressEl || !trendEl) return;

    const rounded = Math.round(Math.min(100, Math.max(0, score)));
    scoreEl.textContent = `${rounded}%`;
    progressEl.style.width = `${rounded}%`;

    // Trend
    const prev = parseInt(localStorage.getItem(`prev_${type}`) || '0');
    const diff = rounded - prev;
    const icon = diff > 0 ? 'fa-arrow-up' : diff < 0 ? 'fa-arrow-down' : 'fa-minus';
    const text = diff !== 0 ? `${Math.abs(diff)}% from last` : 'No previous data';
    trendEl.innerHTML = `<i class="fas ${icon}"></i> <span>${text}</span>`;
    localStorage.setItem(`prev_${type}`, rounded.toString());
  }

    // Sample frame (2/sec, sequential data for backend)
  function sampleFrame(second, frameIndex, landmarks) {
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

    const leftShoulder = landmarks[11], rightShoulder = landmarks[12], leftHip = landmarks[23], rightHip = landmarks[24];
    const features = {
      shoulder_pitch: Math.atan2(rightShoulder.y - leftShoulder.y, rightShoulder.x - leftShoulder.x) * 180 / Math.PI,
      torso_tilt: Math.atan2(rightHip.y - leftHip.y, rightHip.x - leftHip.x) * 180 / Math.PI,
      joint_velocity: previousLandmarks ? Math.hypot(
        leftShoulder.x - previousLandmarks[11].x, leftShoulder.y - previousLandmarks[11].y
      ) * SAMPLING_FPS : 0,
      step_symmetry: Math.abs((leftHip.x - rightHip.x) - (previousLandmarks ? (previousLandmarks[23].x - previousLandmarks[24].x) : 0)),
      quality_score: (Object.keys(visibleLandmarks).length / 33) * 100
    };

    const frameDataItem = {
      second,
      frameIndex,
      landmarks: visibleLandmarks,
      features
    };

    frameData.push(frameDataItem);
    log(`Sampled frame ${frameIndex}s${second} (${frameData.length}/${ANALYSIS_MAX_SAMPLES})`);

    // Optional backend send (no error if 404/offline)
    // if (typeof fetch !== 'undefined') {
    //   fetch('/', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ frame: frameDataItem, stage: 'sample' })
    //   }).catch(err => {
    //     if (DEBUG) error('Backend sample send failed (offline mode):', err);
    //   });
    // }
  }

  // Analysis timer (non-blocking, 2 FPS sampling)
  async function startAnalysisTimer(duration) {
    const totalSamples = Math.min(duration * SAMPLING_FPS, ANALYSIS_MAX_SAMPLES);
    let currentSecond = 1, samplesInSecond = 0;

    // Optional backend start (no error if 404)
    // if (typeof fetch !== 'undefined') {
    //   try {
    //     await fetch('/', {
    //       method: 'POST',
    //       headers: { 'Content-Type': 'application/json' },
    //       body: JSON.stringify({ duration, stage: 'start' })
    //     });
    //     log('Backend started');
    //   } catch (err) {
    //     if (DEBUG) error('Backend start failed (continuing offline):', err);
    //   }
    // }

    sampleInterval = setInterval(() => {
      if (!isAnalyzing || frameData.length >= totalSamples) {
        clearInterval(sampleInterval);
        finalizeAnalysis();
        return;
      }

      if (latestLandmarks.length > 3) {
        samplesInSecond++;
        sampleFrame(currentSecond, samplesInSecond, latestLandmarks);

        // Progress UI (dynamic)
        batchUpdate(() => {
          const progress = Math.min(100, (frameData.length / totalSamples) * 100);
          const progressEl = document.getElementById('analysis-progress');
          if (progressEl) progressEl.style.width = `${progress}%`;
        });

        if (samplesInSecond >= SAMPLING_FPS) {
          currentSecond++;
          samplesInSecond = 0;
        }
      }
    }, 1000 / SAMPLING_FPS);
  }

  // Finalize analysis (updated: Send to backend for LLM report)
async function finalizeAnalysis() {
  isAnalyzing = false;
  clearInterval(sampleInterval);
  stopCamera(); // Uncomment if you want auto-stop after analysis
  const analysisData = {
    metadata: {
      timestamp: new Date().toISOString(),
      duration: parseInt(document.getElementById('time-display')?.textContent || '5'),
      totalFrames: frameData.length
    },
    frames: frameData.slice(0, ANALYSIS_MAX_SAMPLES)
  };

  log('Analysis complete. Frames:', frameData.length);
  console.log('Full JSON Data:', JSON.stringify(analysisData, null, 2));

  

  // Use Puter.js for LLM processing (no backend needed)
  try {
    // Construct the same prompt you were using in the backend
    const prompt = `You are an expert in human movement analysis and biomechanics.
    Analyze the following pose detection data from a user's physical activity session (collected via MediaPipe Pose landmarks).

Data Summary:
- Duration: ${analysisData.metadata.duration} seconds
- Total Frames: ${analysisData.metadata.totalFrames}
- Timestamp: ${analysisData.metadata.timestamp}

Sample Frame Structure (showing landmarks and features for ${analysisData.frames.length} frames):
${JSON.stringify(analysisData.frames.slice(0, 5), null, 2)}  # First 5 frames as example; analyze all implicitly.

Key Features Across Frames (computed from landmarks):
- Landmarks: 33 body points (e.g., nose, shoulders, hips, knees) with x,y,z coordinates and visibility scores.
- Extracted Metrics: shoulder_pitch (degrees), torso_tilt (degrees), joint_velocity (px/s), step_symmetry (difference), quality_score (% visible landmarks).

Generate a comprehensive, professional movement report for the user. Structure it as follows:
1. **Summary**: Overview of session (e.g., overall posture quality, activity efficiency).
2. **Key Metrics**: Break down averages for posture (shoulder alignment), balance (hip/knee stability), symmetry (limb differences), motion (smoothness/velocity).
3. **Insights**: Analyze patterns (e.g., "High shoulder pitch suggests forward lean—potential back strain risk"). Reference specific data (e.g., avg shoulder_pitch: X°).
4. **Recommendations**: Personalized tips (e.g., "Strengthen core for better balance"). Flag risks (e.g., asymmetry >20% may indicate injury).
5. **Overall Score**: 0-100% efficiency rating.

Make it engaging, actionable. Use bullet points/tables for readability. Base analysis strictly on data—be positive and encouraging.`;

    // Use Puter.js AI instead of backend API call
    // report = await puter.ai.chat(prompt, { model: "gpt-5-nano" });
    const apiKey = process.env.skvision;
    report = await callGroqAPI(apiKey, prompt, model);
    
    // Store the report and show the report section
    currentReport = report;
    const reportSection = document.getElementById('report-section');
    if (reportSection) {
      reportSection.style.display = 'block';
    }
    log('LLM Report generated successfully via Puter.js');

  } catch (err) {
    error('Puter.js AI failed:', err);
    log('Falling back to local report generation');
    // Fallback: Generate local report
    // report = generateReport();  // static report
  }

  // Final averages (update UI even if LLM fails)
  if (frameData.length > 0) {
    const avgPosture = frameData.reduce((sum, f) => sum + (100 - Math.abs(f.features?.shoulder_pitch || 0)), 0) / frameData.length;
    const avgQuality = frameData.reduce((sum, f) => sum + (f.features?.quality_score || 50), 0) / frameData.length;
    updateMetricUI('posture', avgPosture);
    updateMetricUI('balance', avgQuality);
    updateMetricUI('symmetry', avgQuality);
    updateMetricUI('motion', avgPosture);
  }

  // Function to call Groq API
            async function callGroqAPI(apiKey, prompt, model) {
                const url = 'https://api.groq.com/openai/v1/chat/completions';
                
                const requestBody = {
                    model: 'llama-3.1-8b-instant',
                    messages: [
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    temperature: 0.7,
                    max_tokens: 1024,
                    top_p: 1,
                    stream: false
                };
                
                const startTime = performance.now();
                
                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${apiKey}`
                        },
                        body: JSON.stringify(requestBody)
                    });
                    
                    const endTime = performance.now();
                    const duration = ((endTime - startTime) / 1000).toFixed(2);
                    
                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error('API Error Response:', errorText);
                        throw new Error(`API request failed with status ${response.status}: ${errorText}`);
                    }
                    
                    const data = await response.json();
                    
                    return {
                        content: data.choices && data.choices.length > 0 ? data.choices[0].message.content : 'No response received',
                        usage: data.usage || {},
                        duration: duration
                    };
                } catch (error) {
                    throw error;
                }
            }
  // Show report in modal
  const reportSection = document.getElementById('report-section');
  if (reportSection) reportSection.style.display = 'block';
  showReportModal(report || 'Analysis complete, but report generation failed. Check console for data.');

  
}

  // Fallback local report generation (your original function, now used only on error)
  function generateReport() {
    if (frameData.length === 0) {
      return 'No analysis data available. Run an analysis first.';
    }

    const duration = document.getElementById('time-display')?.textContent || '5';
    const postureScore = document.getElementById('posture-score')?.textContent || 'N/A';
    const balanceScore = document.getElementById('balance-score')?.textContent || 'N/A';
    const symmetryScore = document.getElementById('symmetry-score')?.textContent || 'N/A';
    const motionScore = document.getElementById('motion-score')?.textContent || 'N/A';

    // Compute averages from collected data
    const avgFeatures = frameData.reduce((acc, frame) => {
      const f = frame.features || {};
      acc.pitch += Math.abs(f.shoulder_pitch || 0);
      acc.tilt += Math.abs(f.torso_tilt || 0);
      acc.quality += f.quality_score || 0;
      acc.velocity += f.joint_velocity || 0;
      acc.symmetry += f.step_symmetry || 0;
      return acc;
    }, { pitch: 0, tilt: 0, quality: 0, velocity: 0, symmetry: 0 });

    const numFrames = frameData.length;
    const avgPitch = Math.round(avgFeatures.pitch / numFrames);
    const avgTilt = Math.round(avgFeatures.tilt / numFrames);
    const avgQuality = Math.round(avgFeatures.quality / numFrames);
    const avgVelocity = Math.round(avgFeatures.velocity / numFrames * 10) / 10;
    const avgSymmetry = Math.round(avgFeatures.symmetry / numFrames * 100) / 100;

    const reportContent = `AI Critical Action Analyzer Report
================================================================================

📊 Analysis Summary
-------------------
- Duration: ${duration} seconds
- Total Frames Analyzed: ${numFrames} (sampled at ${SAMPLING_FPS} FPS)
- Timestamp: ${new Date().toISOString().slice(0, 19).replace('T', ' | ')}
- Device: ${navigator.userAgent.substring(0, 50)}...

🎯 Key Performance Metrics
--------------------------
Posture Score: ${postureScore} | Alignment Quality: ${100 - avgPitch}% (Ideal: >90%)
Balance Score: ${balanceScore} | Stability Deviation: Low (Target: >80%)
Symmetry Score: ${symmetryScore} | Limb Balance: ${avgSymmetry}% symmetry (Ideal: >85%)
Motion Quality: ${motionScore} | Avg Velocity: ${avgVelocity} px/s (Smooth: <5 variance)

📈 Pose & Movement Insights
---------------------------
- Average Shoulder Pitch Deviation: ${avgPitch}° (Recommendation: Keep <10° for optimal posture)
- Average Torso Tilt: ${avgTilt}° (Recommendation: Maintain <5° for balance)
- Landmark Visibility: ${avgQuality}% (Recommendation: Stay fully in frame for accuracy)
- Step/Movement Symmetry: ${avgSymmetry}% (Recommendation: Mirror left/right for efficiency)
- Overall Action Efficiency: ${Math.round((parseInt(postureScore) + parseInt(balanceScore) + parseInt(symmetryScore) + parseInt(motionScore)) / 4)}% 

💡 Personalized Recommendations
-------------------------------
${parseInt(postureScore) > 85 ? '✅ Excellent posture alignment! Continue maintaining straight torso.' : '⚠️ Improve posture: Align shoulders directly over hips to reduce strain.'}
${parseInt(balanceScore) > 80 ? '✅ Strong balance detected. Even weight distribution is effective.' : '⚠️ Enhance balance: Distribute weight evenly between feet to prevent sway.'}
${parseInt(symmetryScore) > 75 ? '✅ Good symmetry in movements. Low risk of overuse injuries.' : '⚠️ Focus on symmetry: Ensure left and right limbs move equally to avoid imbalances.'}
${parseInt(motionScore) > 80 ? '✅ Smooth, efficient motion. Great biomechanics!' : '⚠️ Refine motion: Slow down jerky movements for better control and reduced fatigue.'}

📝 Technical Notes
------------------
- Data collected via MediaPipe Pose (33 landmarks, visibility >${VISIBLE_THRESHOLD}).
- Sampling: ${SAMPLING_FPS} frames/second for ${duration}s.
- Full dataset logged in browser console (JSON format).
- For professional assessment, consult a certified trainer or physiotherapist.

Generated by AI Critical Action Analyzer | Stay Active & Balanced! 🚀
================================================================================`;

    return reportContent;
  }

  // Modal functions for displaying LLM/local report
  // Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Connect the generate report button
  const generateReportBtn = document.getElementById('generate-report-btn');
  if (generateReportBtn) {
    generateReportBtn.addEventListener('click', showStoredReport);
  }
  
  // Connect download button
  const downloadBtn = document.getElementById('download-report-btn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadReport);
  }
  
  // Connect close button
  const closeBtn = document.getElementById('close-report-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeReportModal);
  }
});

// Store the latest report globally
let currentReport = '';

function showReportModal(reportContent) {
  const modal = document.getElementById('llm-report-modal');
  const contentEl = document.getElementById('llm-report-content');
  const closeBtn = document.querySelector('#llm-report-modal .close');

  if (!modal || !contentEl) {
    // Fallback: Alert if modal HTML missing
    alert(reportContent);
    return;
  }

  // Store the report
  currentReport = reportContent;
  
  // Format the report content with HTML
  contentEl.innerHTML = reportContent;
  modal.style.display = 'block';

  // Close handlers
  closeBtn.onclick = closeReportModal;
  modal.onclick = (e) => { 
    if (e.target === modal) closeReportModal(); 
  };
}

// Show stored report when button is clicked
function showStoredReport() {
  if (currentReport) {
    showReportModal(currentReport);
  } else {
    alert('No report available. Please complete an analysis first.');
  }
}

// Format the report content with beautiful HTML
function formatReportContent(reportText) {
  if (!reportText) return '<p>No report content available.</p>';
  
  // Convert markdown-like formatting to HTML
  let html = reportText
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/## (.*?)(?=\n|$)/g, '<h3>$1</h3>')
    .replace(/# (.*?)(?=\n|$)/g, '<h2>$1</h2>')
    .replace(/\n/g, '<br>')
    .replace(/- (.*?)(?=\n|$)/g, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/(\d+\/100)/g, '<div class="score">Overall Score: $1</div>')
    .replace(/(\d+%)/g, '<span class="percentage">$1</span>');
  
  return html;
}

function closeReportModal() {
  const modal = document.getElementById('llm-report-modal');
  if (modal) modal.style.display = 'none';
}

// Download report as text file
function downloadReport() {
  if (!currentReport) return;
  
  const blob = new Blob([currentReport], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `movement-analysis-report-${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Global escape key for modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeReportModal();
  }
});

  // Start camera & analysis
  async function startCamera() {
    log('Starting analysis');
    if (isAnalyzing) return log('Already analyzing');

    video = document.querySelector('.input_video');
    canvas = document.querySelector('.output_canvas');
    if (!video || !canvas) {
      error('Missing video/canvas elements');
      alert('Required HTML elements missing. Check structure.');
      return;
    }

    ctx = canvas.getContext('2d');
    if (!ctx) {
      error('Canvas context failed');
      alert('Canvas setup error. Refresh page.');
      return;
    }

    const duration = parseInt(document.getElementById('time-display')?.textContent || '5');

    try {
      // Reset state
      frameData = [];
      previousLandmarks = null;
      latestLandmarks = [];
      noPoseTimer = 0;
      fpsCounter = { frames: 0, lastTime: 0 };
      window.lastVel = 0;

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        const overlayEl = document.getElementById('skeleton-overlay');
        const cameraOverlayEl = document.getElementById('camera-overlay');
        const startBtn = document.getElementById('start-camera');
        const stopBtn = document.getElementById('stop-camera');
        const captureBtn = document.getElementById('capture-frame');
        if (statusEl) statusEl.textContent = 'Initializing...';
        if (indicatorEl) indicatorEl.className = 'indicator-dot yellow';
        if (overlayEl) overlayEl.style.display = 'block';
        if (cameraOverlayEl) cameraOverlayEl.style.display = 'none';
        if (startBtn) startBtn.disabled = true;
        if (stopBtn) stopBtn.disabled = false;
        if (captureBtn) captureBtn.disabled = false;
      });

      // Wait for video ready
      await new Promise(resolve => {
        if (video.readyState >= 1) resolve();
        else {
          const onLoaded = () => {
            video.removeEventListener('loadedmetadata', onLoaded);
            resolve();
          };
          video.addEventListener('loadedmetadata', onLoaded);
          setTimeout(resolve, 100); // Fallback
        }
      });

      // Set canvas size (mobile optimized)
      const targetWidth = window.innerWidth < 768 ? 320 : 640;
      const targetHeight = window.innerWidth < 768 ? 240 : 480;
      canvas.width = targetWidth;
      canvas.height = targetHeight;
      canvas.style.width = `${targetWidth}px`;
      canvas.style.height = `${targetHeight}px`;

      // getUser Media (no space)
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera API not supported. Use modern browser.');
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: targetWidth },
          height: { ideal: targetHeight },
          facingMode: 'user' // Front camera
        }
      });
      video.srcObject = stream;

      // Camera init
      camera = new Camera(video, {
        onFrame: async () => {
          if (pose && isAnalyzing) {
            await pose.send({ image: video });
          }
        },
        width: targetWidth,
        height: targetHeight
      });
      await camera.start();

      log(`Camera active at ${targetWidth}x${targetHeight}`);

      // Skeleton (lazy init)
      if (!skeletonCanvas) initSkeleton();

      isAnalyzing = true;

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        if (statusEl) statusEl.textContent = 'Active';
        if (indicatorEl) indicatorEl.className = 'indicator-dot green';
      });

      // Start timer
      startAnalysisTimer(duration);

    } catch (err) {
      error('Start failed:', err);
      let msg = 'Analysis start failed. ';
      if (err.name === 'NotAllowedError') msg += 'Allow camera access.';
      else if (err.name === 'NotFoundError') msg += 'No camera found.';
      else msg += err.message || 'Unknown error.';
      alert(msg);

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        const startBtn = document.getElementById('start-camera');
        if (statusEl) statusEl.textContent = 'Error';
        if (indicatorEl) indicatorEl.className = 'indicator-dot red';
        if (startBtn) startBtn.disabled = true;
      });
      isAnalyzing = false; // Fixed: was true before
    }
  }

    // Stop (manual or auto)
  function stopCamera() {
    log('Stopping analysis');
    // Cancel animation frame for immediate stop
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }

    // Camera stop (safe check)
    if (camera && typeof camera.stop === 'function') {
      camera.stop();
      camera = null;
    }

    if (sampleInterval) {
      clearInterval(sampleInterval);
      sampleInterval = null;
    }

    // Stop stream tracks
    if (video && video.srcObject) {
      video.srcObject.getTracks().forEach(track => track.stop());
      video.srcObject = null;
      video.pause();
    }
    
    isAnalyzing = false;

    batchUpdate(() => {
      const startBtn = document.getElementById('start-camera');
      const stopBtn = document.getElementById('stop-camera');
      const captureBtn = document.getElementById('capture-frame');
      const statusEl = document.getElementById('camera-status');
      const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
      const overlayEl = document.getElementById('skeleton-overlay');
      if (startBtn) startBtn.disabled = false;
      if (stopBtn) stopBtn.disabled = true;
      if (captureBtn) captureBtn.disabled = true;
      if (statusEl) statusEl.textContent = 'Stopped';
      if (indicatorEl) indicatorEl.className = 'indicator-dot red';
      if (overlayEl) overlayEl.style.display = 'block';

      // Clear skeleton
      if (skeletonCtx && skeletonCanvas) {
        skeletonCtx.clearRect(0, 0, skeletonCanvas.width, skeletonCanvas.height);
        drawStaticHuman2D();
      }
    });

    previousLandmarks = null;
    latestLandmarks = [];
    log('Analysis stopped');
  }

  // Reset (initial state)
  function resetData() {
    log('Resetting to initial state');
    stopCamera();
    frameData = [];

    if (ctx && canvas) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Skeleton reset
    if (skeletonCtx && skeletonCanvas) {
      skeletonCtx.clearRect(0, 0, skeletonCanvas.width, skeletonCanvas.height);
      drawStaticHuman2D();
    }

    batchUpdate(() => {
      const cameraOverlayEl = document.getElementById('camera-overlay');
      const statusEl = document.getElementById('camera-status');
      const skeletonIndicatorEl = document.querySelector('.skeleton-indicator .indicator-dot');

      if (cameraOverlayEl) cameraOverlayEl.style.display = 'block';
      if (statusEl) statusEl.textContent = 'Camera Off';
      if (skeletonIndicatorEl) skeletonIndicatorEl.className = 'indicator-dot red';

      // Reset metrics
      ['posture', 'balance', 'symmetry', 'motion'].forEach(type => {
        const scoreEl = document.getElementById(`${type}-score`);
        const progressEl = document.getElementById(`${type}-progress`);
        const trendEl = document.getElementById(`${type}-trend`);
        if (scoreEl) scoreEl.textContent = '0%';
        if (progressEl) progressEl.style.width = '0%';
        if (trendEl) trendEl.innerHTML = '<i class="fas fa-minus"></i> <span>No previous data</span>';
        localStorage.removeItem(`prev_${type}`);
      });
      
      const landmarksEl = document.getElementById('landmarks-count');
      const confEl = document.getElementById('confidence-score');
      const fpsEl = document.getElementById('frame-rate');
      const reportSection = document.getElementById('report-section');
      const progressEl = document.getElementById('analysis-progress');
      if (landmarksEl) landmarksEl.textContent = '0';
      if (confEl) confEl.textContent = '0%';
      if (fpsEl) fpsEl.textContent = '0 FPS';
      if (reportSection) reportSection.style.display = 'none';
      if (progressEl) progressEl.style.width = '0%';
    });

    fpsCounter = { frames: 0, lastTime: 0 };
    log('Reset complete');
  }

  // Capture frame (optional utility)
  function captureFrame() {
    if (!canvas || !isAnalyzing) {
      alert('No active frame. Start analysis first.');
      return;
    }

    const link = document.createElement('a');
    link.download = `pose-frame-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    log('Frame captured');
  }

  // Timer slider (default 5s, user selectable)
  const timeSlider = document.getElementById('analysis-time-slider');
  const timeDisplay = document.getElementById('time-display');
  const selectedTimeValue = document.getElementById('selected-time-value');
  if (timeSlider && timeDisplay && selectedTimeValue) {
    timeSlider.min = 3;
    timeSlider.max = 30;
    timeSlider.value = 5; // Default
    timeDisplay.textContent = '5';
    selectedTimeValue.textContent = '5 seconds';
    timeSlider.addEventListener('input', (e) => {
      const value = parseInt(e.target.value);
      timeDisplay.textContent = value;
      selectedTimeValue.textContent = `${value} seconds`;
    });
  } else {
    // Fallback if elements missing
    if (timeDisplay) timeDisplay.textContent = '5';
  }

  // Event listeners (core buttons)
  const startBtn = document.getElementById('start-camera');
  if (startBtn) {
    startBtn.addEventListener('click', startCamera);
    log('Start button ready');
  }

  const stopBtn = document.getElementById('stop-camera');
  if (stopBtn) {
    stopBtn.addEventListener('click', stopCamera);
    log('Stop button ready');
  }

  const resetBtn = document.getElementById('reset-data');
  if (resetBtn) {
    resetBtn.addEventListener('click', resetData);
    log('Reset button ready');
  }

  const captureBtn = document.getElementById('capture-frame');
  if (captureBtn) {
    captureBtn.addEventListener('click', captureFrame);
    log('Capture button ready');
  }

  const reportBtn = document.getElementById('generate-report-btn');
  if (reportBtn) {
    reportBtn.addEventListener('click', () => {
      const localReport = generateReport();
      showReportModal(localReport);
    });
    log('Report button ready (fallback local)');
  }

  // Hero button (scroll + start)
  const heroBtn = document.getElementById('hero-analysis-btn');
  if (heroBtn) {
    heroBtn.addEventListener('click', () => {
      const analysisSection = document.getElementById('analysis');
      if (analysisSection) {
        analysisSection.scrollIntoView({ behavior: 'smooth' });
      }
      setTimeout(startCamera, 500); // Delay for smooth scroll
    });
    log('Hero button ready');
  }

  // Keyboard controls (Space: toggle start/stop, R: reset, G: generate local report)
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName.match(/^(INPUT|TEXTAREA|BUTTON)$/i) || e.target.isContentEditable) return;

    switch (e.key.toLowerCase()) {
      case ' ':
        e.preventDefault();
        if (isAnalyzing) {
          stopCamera();
        } else {
          startCamera();
        }
        startBtn?.focus(); // Accessibility
        break;
      case 'r':
        e.preventDefault();
        resetData();
        resetBtn?.focus();
        break;
      case 'g':
        e.preventDefault();
        const localReport = generateReport();
        showReportModal(localReport);
        break;
      case 'escape':
        if (isAnalyzing) stopCamera();
        else closeReportModal(); // Also closes modal
        break;
    }
  });

  // Cleanup on page unload (prevent memory leaks)
  window.addEventListener('beforeunload', () => {
    stopCamera();
    resetData();
    if (camera && typeof camera.stop === 'function') camera.stop();
    if (sampleInterval) clearInterval(sampleInterval);
    if (rafId) cancelAnimationFrame(rafId);
  });

  // Initial UI setup (reset to default state)
  batchUpdate(() => {
    const cameraOverlayEl = document.getElementById('camera-overlay');
    const statusEl = document.getElementById('camera-status');
    const indicators = document.querySelectorAll('.indicator-dot');
    const stats = document.querySelectorAll('.stat-value, .progress-fill');
    const trends = document.querySelectorAll('[id$="-trend"]');
    const reportSection = document.getElementById('report-section');
    const progressEl = document.getElementById('analysis-progress');

    if (cameraOverlayEl) cameraOverlayEl.style.display = 'block';
    if (statusEl) statusEl.textContent = 'Camera Off';

    indicators.forEach(el => el.className = 'indicator-dot red');
    stats.forEach(el => {
      if (el.classList.contains('stat-value')) el.textContent = '0%';
      else if (el.classList.contains('progress-fill')) el.style.width = '0%';
    });
    trends.forEach(el => el.innerHTML = '<i class="fas fa-minus"></i> <span>No previous data</span>');

    if (reportSection) reportSection.style.display = 'none';
    if (progressEl) progressEl.style.width = '0%';

    // Clear trends in localStorage
    ['posture', 'balance', 'symmetry', 'motion'].forEach(type => localStorage.removeItem(`prev_${type}`));
  });

  // Pre-initialize (non-blocking)
  initSkeleton(); // Setup skeleton (2D fallback if WebGL fails)
  log('AI Critical Action Analyzer fully initialized');
  log('Ready for analysis. Select timer, click Start, and perform actions in frame.');
});
