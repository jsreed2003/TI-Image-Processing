# FastAPI Backend Setup Guide

Complete guide to set up and integrate the FastAPI backend with your React Native app.

## 📋 Table of Contents

1. [Backend Setup](#backend-setup)
2. [Testing the Backend](#testing-the-backend)
3. [React Native Integration](#react-native-integration)
4. [Troubleshooting](#troubleshooting)
5. [Production Deployment](#production-deployment)

---

## 🚀 Backend Setup

### Step 1: Install Python and Dependencies

**Check Python version:**
```bash
python --version  # Should be 3.8 or higher
```

**Create project directory:**
```bash
cd /path/to/your/project
mkdir fastapi-backend
cd fastapi-backend
```

**Create virtual environment:**
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### Step 2: Add Your Algorithm Code

The `main.py` file has placeholders for your algorithm functions. You need to copy your code from the Jupyter notebook:

1. Open `main.py`
2. Find the section marked `# YOUR EXISTING ALGORITHM CODE`
3. Copy these functions from your notebook:
   - `getTopLeft()`
   - `refineEdgePoint()`
   - `findLineIntersection()`
   - `detectCorners()`
   - `findBiggestRectangle()`
   - `calculateHomography()`

**The functions are already included in the provided `main.py`!** But if you've made improvements to your algorithm, update them.

### Step 3: Start the Server

```bash
# Development mode (auto-reload on code changes)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or simply:
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 4: Verify It's Working

Open browser to:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

You should see a beautiful Swagger UI interface!

---

## 🧪 Testing the Backend

### Option 1: Use the Interactive Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on `POST /api/detect_corners`
3. Click "Try it out"
4. Click "Choose File" and select a test image
5. Click "Execute"
6. See the response below

### Option 2: Use the Test Script

```bash
# Make sure you have a test image
python test_api.py
```

This will run all tests and show you if everything is working.

### Option 3: Use cURL

```bash
curl -X POST "http://localhost:8000/api/detect_corners" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/test_image.jpg"
```

### Expected Response

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

---

## 📱 React Native Integration

### Step 1: Find Your Computer's IP Address

**macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig
```

Look for IPv4 Address under your WiFi adapter (usually starts with `192.168.` or `10.`)

Example: `192.168.1.100`

### Step 2: Update API Configuration

Open `src/api/keystoneAPI.js` and update:

```javascript
const API_URL = 'http://192.168.1.100:8000'; // Your computer's IP
```

**Important:**
- ✅ Use your actual IP address
- ✅ Phone and computer must be on same WiFi
- ✅ Keep port 8000
- ❌ Don't use `localhost` (won't work on phone)

**Special cases:**
- **Android Emulator:** Use `http://10.0.2.2:8000`
- **iOS Simulator:** Use `http://localhost:8000`

### Step 3: Test Connection from React Native

Add this to your HomeScreen to test the connection:

```javascript
import {testConnection} from '../api/keystoneAPI';

// In HomeScreen component:
useEffect(() => {
  testConnection();
}, []);
```

Check the console logs:
- ✅ "API connection successful" → You're good!
- ❌ "Connection failed" → See troubleshooting below

### Step 4: The Integration is Already Done!

The `ProcessingScreen.js` has been updated to use the real API:

```javascript
// Import API
const {detectCorners} = require('../api/keystoneAPI');

// Call API
const result = await detectCorners(imageUri);

// Navigate with results
navigation.replace('Results', {
  imageUri,
  corners: result,
});
```

### Step 5: Test End-to-End

1. **Start FastAPI server:**
   ```bash
   cd fastapi-backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python main.py
   ```

2. **Start React Native app:**
   ```bash
   cd keystone-app-starter
   npm start
   ```

3. **Run on device:**
   ```bash
   npm run ios
   # or
   npm run android
   ```

4. **Test the flow:**
   - Open app
   - Tap "Start Camera"
   - Take a picture of projector output
   - See processing screen
   - View results!

---

## 🐛 Troubleshooting

### Problem: "Network request failed"

**Causes:**
- Phone and computer not on same WiFi
- Wrong IP address in `keystoneAPI.js`
- Firewall blocking port 8000
- Server not running

**Solutions:**
1. **Check WiFi:**
   - Phone settings → WiFi → Note network name
   - Computer → Check connected to same network

2. **Verify IP address:**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```
   Update `API_URL` in `keystoneAPI.js`

3. **Check firewall:**
   - macOS: System Preferences → Security & Privacy → Firewall → Allow port 8000
   - Windows: Windows Defender → Allow app through firewall → Python
   
4. **Verify server is running:**
   Open browser to `http://YOUR_IP:8000/health`

### Problem: "Could not find chessboard pattern"

**Causes:**
- Projector not displaying checkerboard
- Image doesn't show all 4 corners
- Image is blurry or dark

**Solutions:**
1. Make sure projector displays 8x8 checkerboard:
   - In TI's DLP GUI: Display → Patterns → Checkerboard
   - Foreground: Black, Background: White

2. Capture better images:
   - Include all 4 corners
   - Good lighting
   - Sharp focus (not blurry)
   - Don't use zoom < 1.0x

3. Test with a known good image first

### Problem: CORS errors in browser

**This shouldn't happen** since we enabled CORS, but if it does:

In `main.py`, verify:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problem: Server crashes with error

**Common errors:**

1. **"Address already in use"**
   ```bash
   # Kill process on port 8000
   # macOS/Linux:
   lsof -ti:8000 | xargs kill -9
   
   # Windows:
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **"No module named 'fastapi'"**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **"OpenCV not found"**
   ```bash
   pip install opencv-python==4.9.0.80
   ```

### Problem: Slow processing

**Solutions:**

1. **Downscale images before sending:**
   ```javascript
   // In React Native, before sending to API
   const resizedImage = await ImageManipulator.manipulateAsync(
     imageUri,
     [{ resize: { width: 1920 } }],
     { compress: 0.8, format: SaveFormat.JPEG }
   );
   ```

2. **Optimize algorithm:**
   - Add image downscaling in `main.py`
   - Use async processing
   - Cache results

---

## 🚀 Production Deployment

### Option 1: Run on University Server

If you have access to a university server:

1. **Install on server:**
   ```bash
   ssh user@server.university.edu
   git clone your-repo
   cd fastapi-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run with systemd or supervisor:**
   ```bash
   # Using gunicorn for production
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Update React Native:**
   ```javascript
   const API_URL = 'http://server.university.edu:8000';
   ```

### Option 2: Deploy to Cloud (Heroku Example)

1. **Create `Procfile`:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy:**
   ```bash
   heroku create keystone-api
   git push heroku main
   ```

3. **Update React Native:**
   ```javascript
   const API_URL = 'https://keystone-api.herokuapp.com';
   ```

### Option 3: Use Ngrok (Temporary Testing)

Perfect for testing with team members:

1. **Install ngrok:**
   ```bash
   brew install ngrok  # macOS
   # or download from ngrok.com
   ```

2. **Start server:**
   ```bash
   python main.py
   ```

3. **In another terminal:**
   ```bash
   ngrok http 8000
   ```

4. **Use the ngrok URL:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:8000
   ```
   
   Update `keystoneAPI.js`:
   ```javascript
   const API_URL = 'https://abc123.ngrok.io';
   ```

5. **Share URL with team!**

---

## 📊 Performance Benchmarks

Expected processing times (on M1 Mac):
- Health check: ~10ms
- Corner detection: ~500-1500ms
- Full processing: ~800-2000ms

Times will vary based on:
- Image size
- Computer speed
- Network latency (phone ↔ computer)

---

## 🔒 Security Considerations

### For Development
- ✅ CORS enabled for all origins
- ✅ No authentication required
- ⚠️ Anyone on WiFi can access API

### For Production
- Add API key authentication
- Restrict CORS to specific domains
- Add rate limiting
- Use HTTPS
- Validate file uploads
- Implement logging and monitoring

---

## 📝 Next Steps

1. ✅ Backend running
2. ✅ API tested
3. ✅ React Native integrated
4. [ ] Test with real projector images
5. [ ] Optimize performance
6. [ ] Add error recovery
7. [ ] Deploy to production (optional)

---

## 🆘 Getting Help

**Check logs:**
```bash
# FastAPI server logs
# Just look at terminal where server is running

# React Native logs
npx react-native log-android
npx react-native log-ios
```

**Common commands:**
```bash
# Restart FastAPI server
# Press Ctrl+C, then:
python main.py

# Restart React Native
# Press 'r' in Metro bundler

# Clear React Native cache
npm start -- --reset-cache
```

**Still stuck?**
1. Check all logs
2. Verify network connection
3. Test with curl/Postman
4. Ask team members
5. Check FastAPI docs: https://fastapi.tiangolo.com/

---

**Good luck! 🚀**
