/**
 * Keystone Correction API client for Capacitor (web context).
 * Converts base64 image strings to Blob before uploading.
 *
 * API_URL is auto-injected at build time from .env (VITE_API_URL).
 * Run `npm run build` — the prebuild script sets it to the current machine's IP.
 */
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function base64ToBlob(base64, mimeType = 'image/jpeg') {
  const byteString = atob(base64);
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: mimeType });
}

/**
 * Send a base64-encoded JPEG to the backend for corner detection.
 * @param {string} base64Image - Raw base64 string (no data URI prefix)
 * @param {object} settings - { chessboardCols, chessboardRows, aspectRatio }
 * @returns {Promise<{originalCorners, optimalCorners, imageWidth, imageHeight}>}
 */
export const detectCorners = async (base64Image, settings = {}) => {
  const {
    chessboardCols = 8,
    chessboardRows = 8,
    aspectRatio = '16:9',
  } = settings;

  // Convert "16:9" string to a decimal number for the backend
  const [w, h] = aspectRatio.split(':').map(Number);
  const aspectRatioDecimal = w / h;

  const blob = base64ToBlob(base64Image);
  const formData = new FormData();
  formData.append('file', blob, 'capture.jpg');
  formData.append('cols', String(chessboardCols));
  formData.append('rows', String(chessboardRows));
  formData.append('aspect_ratio', String(aspectRatioDecimal));

  const response = await fetch(`${API_URL}/api/detect_corners`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Server error ${response.status}`);
  }

  const data = await response.json();
  if (!data.success) {
    throw new Error(data.message || 'Corner detection was not successful');
  }

  return {
    originalCorners: data.originalCorners,
    optimalCorners: data.optimalCorners,
    optimalInputCorners: data.optimalInputCorners,
    imageWidth: data.imageWidth,
    imageHeight: data.imageHeight,
  };
};

/** Quick health check — resolves true if the server is reachable. */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === 'healthy' || data.status === 'ok';
  } catch {
    return false;
  }
};
