/**
 * Keystone API Client
 * Handles communication with FastAPI backend
 */

// CONFIGURATION
// Replace with your computer's IP address (find using ipconfig/ifconfig)
// Make sure your phone and computer are on the same WiFi network
const API_URL = 'http://192.168.1.100:8000'; // UPDATE THIS!

// For Android emulator, use: 'http://10.0.2.2:8000'
// For iOS simulator, use: 'http://localhost:8000'

/**
 * Detect corners in projector output image
 * 
 * @param {string} imageUri - URI of the captured image
 * @returns {Promise<Object>} Corner detection results
 */
export const detectCorners = async (imageUri) => {
  try {
    // Create form data
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'projection.jpg',
    });

    console.log('Sending image to API:', API_URL);

    // Send request
    const response = await fetch(`${API_URL}/api/detect_corners`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json',
      },
    });

    // Check response
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Corner detection failed');
    }

    const data = await response.json();

    // Validate response
    if (!data.success) {
      throw new Error(data.message || 'Corner detection was not successful');
    }

    console.log('Corner detection successful:', data);

    return {
      originalCorners: data.originalCorners,
      optimalCorners: data.optimalCorners,
      imageWidth: data.imageWidth,
      imageHeight: data.imageHeight,
    };
  } catch (error) {
    console.error('API Error:', error);
    
    // Provide user-friendly error messages
    if (error.message.includes('Network request failed')) {
      throw new Error(
        'Cannot connect to server. Make sure:\n' +
        '1. FastAPI server is running\n' +
        '2. Phone and computer are on same WiFi\n' +
        '3. API_URL is set correctly'
      );
    } else if (error.message.includes('Could not find chessboard')) {
      throw new Error(
        'Could not detect checkerboard pattern. Make sure:\n' +
        '1. Projector is displaying checkerboard\n' +
        '2. All 4 corners are visible\n' +
        '3. Image is clear and well-lit'
      );
    }
    
    throw error;
  }
};

/**
 * Full image processing with additional metadata
 * 
 * @param {string} imageUri - URI of the captured image
 * @returns {Promise<Object>} Full processing results
 */
export const processImage = async (imageUri) => {
  try {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'projection.jpg',
    });

    const response = await fetch(`${API_URL}/api/process_image`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Image processing failed');
    }

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.message || 'Processing was not successful');
    }

    return result.data;
  } catch (error) {
    console.error('Processing Error:', error);
    throw error;
  }
};

/**
 * Health check to verify API is running
 * 
 * @returns {Promise<boolean>} True if API is healthy
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    return data.status === 'healthy' || data.status === 'ok';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

/**
 * Get API configuration
 */
export const getAPIConfig = () => {
  return {
    baseURL: API_URL,
    timeout: 30000, // 30 seconds
  };
};

/**
 * Test API connection
 * Useful for debugging
 */
export const testConnection = async () => {
  try {
    console.log('Testing API connection to:', API_URL);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${API_URL}/health`, {
      method: 'GET',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      console.log('✅ API connection successful');
      return true;
    } else {
      console.log('❌ API returned error:', response.status);
      return false;
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('❌ Connection timeout');
    } else {
      console.log('❌ Connection failed:', error.message);
    }
    return false;
  }
};

export default {
  detectCorners,
  processImage,
  checkHealth,
  getAPIConfig,
  testConnection,
};
