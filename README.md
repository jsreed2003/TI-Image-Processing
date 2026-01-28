# FastAPI Backend for Keystone Correction

REST API server that processes projector images and returns corner detection results.

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or simply:
python main.py
```

Server will be available at:
- API: `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## 📡 API Endpoints

### 1. Health Check
```bash
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "All systems operational"
}
```

### 2. Detect Corners (Main Endpoint)
```bash
POST /api/detect_corners
Content-Type: multipart/form-data
```

**Request:**
- `file`: Image file (JPEG/PNG) of projector output

**Response:**
```json
{
  "originalCorners": [
    [150.5, 80.2],
    [3650.1, 100.5],
    [3600.8, 2050.3],
    [180.2, 2000.1]
  ],
  "optimalCorners": [
    [120.0, 45.0],
    [3710.0, 52.0],
    [3698.0, 2103.0],
    [132.0, 2096.0]
  ],
  "success": true,
  "message": "Corner detection successful",
  "imageWidth": 3840,
  "imageHeight": 2160
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/detect_corners" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@projection_image.jpg"
```

### 3. Process Image (Extended)
```bash
POST /api/process_image
```

Returns additional metadata including optimal input corners for the projector.

## 🔧 Integration with React Native

### Update the React Native API client

Create `src/api/keystoneAPI.js`:

```javascript
const API_URL = 'http://YOUR_COMPUTER_IP:8000';

export const detectCorners = async (imageUri) => {
  try {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'projection.jpg',
    });

    const response = await fetch(`${API_URL}/api/detect_corners`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Corner detection failed');
    }

    const data = await response.json();
    return {
      originalCorners: data.originalCorners,
      optimalCorners: data.optimalCorners,
    };
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

### Update ProcessingScreen.js

```javascript
import {detectCorners} from '../api/keystoneAPI';

// In the processImage function:
try {
  setStatusText('Analyzing image...');
  setProgress(20);

  setStatusText('Detecting corners...');
  setProgress(40);
  
  // Call actual API
  const result = await detectCorners(imageUri);
  
  setStatusText('Calculating correction...');
  setProgress(80);
  
  setStatusText('Complete!');
  setProgress(100);
  
  navigation.replace('Results', {
    imageUri,
    corners: result,
  });
} catch (err) {
  setError(err.message);
}
```

## 🧪 Testing the API

### Using the Interactive Docs

1. Start the server
2. Open browser to `http://localhost:8000/docs`
3. Click on `POST /api/detect_corners`
4. Click "Try it out"
5. Upload an image file
6. Click "Execute"
7. See the response

### Using Python

```python
import requests

url = "http://localhost:8000/api/detect_corners"
files = {"file": open("test_image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Using Postman

1. Create new POST request
2. URL: `http://localhost:8000/api/detect_corners`
3. Body → form-data
4. Key: `file` (change type to File)
5. Value: Select your image file
6. Send

## 📱 Testing from React Native App

### Find Your Computer's IP Address

**macOS/Linux:**
```bash
ifconfig | grep "inet "
```

**Windows:**
```bash
ipconfig
```

Look for your local IP (usually starts with `192.168.` or `10.`)

### Update React Native Code

In `src/api/keystoneAPI.js`, replace `YOUR_COMPUTER_IP`:

```javascript
// If your computer IP is 192.168.1.100:
const API_URL = 'http://192.168.1.100:8000';
```

### Important: Same Network

- Your phone and computer must be on the **same WiFi network**
- Firewall may block connections - add exception for port 8000
- On Android emulator, use `10.0.2.2` instead of localhost

## 🐛 Troubleshooting

### Error: "Could not find chessboard pattern"

**Cause:** Image doesn't contain the checkerboard pattern or corners aren't visible

**Solution:**
- Make sure projector is displaying 8x8 checkerboard
- Ensure all 4 corners are visible in the image
- Check image quality (focus, lighting)

### Error: "Connection refused"

**Cause:** Server not running or wrong IP address

**Solution:**
- Make sure FastAPI server is running
- Check IP address is correct
- Make sure port 8000 isn't blocked by firewall

### Error: "CORS policy blocked"

**Already handled!** The server has CORS enabled for all origins.

## 🔒 Security Notes

### For Production

1. **Restrict CORS origins:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

2. **Add API key authentication:**
```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/api/detect_corners", dependencies=[Depends(verify_api_key)])
async def detect_corners_endpoint(...):
    ...
```

3. **Add rate limiting:**
```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/detect_corners")
@limiter.limit("10/minute")
async def detect_corners_endpoint(...):
    ...
```

## 📊 Performance Optimization

### For Faster Processing

1. **Downscale large images:**
```python
MAX_SIZE = 1920  # Maximum dimension

if max(img.shape[:2]) > MAX_SIZE:
    scale = MAX_SIZE / max(img.shape[:2])
    img = cv2.resize(img, None, fx=scale, fy=scale)
```

2. **Use async processing:**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.post("/api/detect_corners")
async def detect_corners_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    # Run CPU-intensive work in thread pool
    result = await asyncio.get_event_loop().run_in_executor(
        executor,
        process_image,
        contents
    )
    return result
```

## 🚀 Deployment Options

### Option 1: Cloud Deployment (Heroku, AWS, GCP)
- Deploy FastAPI to cloud server
- Update API_URL in React Native to cloud URL
- Suitable for production

### Option 2: Local Network (Current Setup)
- Run on your computer
- Only works on same WiFi
- Good for development/testing

### Option 3: Ngrok (Temporary Public URL)
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Run server
python main.py

# In another terminal:
ngrok http 8000

# Use the ngrok URL in your React Native app
```

## 📝 Logging

Logs are printed to console. To save to file:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

## 🧩 Next Steps

1. ✅ Server is running
2. [ ] Test with sample images
3. [ ] Update React Native app to use this API
4. [ ] Test end-to-end flow
5. [ ] Optimize performance if needed
6. [ ] Deploy to production (optional)

## 📞 Support

- FastAPI docs: https://fastapi.tiangolo.com/
- OpenCV docs: https://docs.opencv.org/
- Issues: Contact your team

---

**Last Updated:** January 26, 2026  
**Version:** 1.0.0
