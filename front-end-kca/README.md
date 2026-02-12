# Keystone Correction App - Frontend

Mobile application for Texas Instruments DLP Projector keystone correction. Built with React, Vite, and Capacitor for iOS/Android.

---

## 📱 Overview

This app allows users to capture images of projected chessboard patterns and send them to a backend server for keystone correction calculation. The app provides a live camera preview with alignment guides and displays the detected corner coordinates.

**Tech Stack:**
- React 18.2
- Vite 4.5 (Node 18 compatible)
- Capacitor 6.2 (iOS/Android wrapper)
- capacitor-camera-view 1.0.0 (live camera preview)

---

## 🚀 Prerequisites

- **Node.js**: v18.13.0 (Required - do not upgrade)
- **npm**: Comes with Node.js
- **iOS Development:**
  - macOS with Xcode installed
  - iOS device or simulator
- **Android Development:**
  - Android Studio
  - Android device or emulator

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd keystone-correction-app
```

### 2. Install Dependencies
```bash
npm install --legacy-peer-deps
```

**Note:** We use `--legacy-peer-deps` due to specific version requirements for Node 18 compatibility.

### 3. Build the Web App
```bash
npm run build
```

---

## 🔧 Platform Setup

### iOS Setup
```bash
# Add iOS platform (if not already added)
npx cap add ios

# Sync web assets to iOS
npx cap sync ios

# Install CocoaPods dependencies
cd ios/App
pod install
cd ../..

# Open in Xcode
npx cap open ios
```

**In Xcode:**
1. Select your connected iPhone from device dropdown
2. Update Bundle Identifier if needed (under Signing & Capabilities)
3. Click Play button (Cmd + R) to build and run

### Android Setup
```bash
# Add Android platform (if not already added)
npx cap add android

# Sync web assets to Android
npx cap sync android

# Open in Android Studio
npx cap open android
```

**In Android Studio:**
1. Wait for Gradle sync to complete
2. Select your connected Android device or emulator
3. Click Run button to build and install

---

## 🎨 App Features

### Current Features
- ✅ Live camera preview with transparent UI overlay
- ✅ TI red branding (#CC0000)
- ✅ Settings page (aspect ratio, chessboard parameters)
- ✅ Info page (usage instructions, camera positioning guidance)
- ✅ Image capture with high quality (90% JPEG)
- ✅ Results page displaying captured image
- ✅ Crosshair alignment guide

### Planned Features
- [ ] Backend integration for corner detection
- [ ] Visual corner overlay on results (red rectangle)
- [ ] Live feedback during camera alignment
- [ ] Error handling and loading states
- [ ] Android build and testing

---

## 🔗 Backend Integration

### API Configuration

The app expects a backend server running Jackson's FastAPI corner detection API.

**Update backend URL in `src/components/CameraScanner.jsx`:**
```javascript
const BACKEND_URL = 'http://YOUR_BACKEND_IP:8000';
```

### Expected Backend Endpoint
```
POST /api/detect_corners
Content-Type: multipart/form-data

Request:
- file: Image file (JPEG)

Response:
{
  "originalCorners": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
  "optimalCorners": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
  "success": true,
  "message": "Corner detection successful",
  "imageWidth": 3840,
  "imageHeight": 2160
}
```

### Testing Locally

1. Make sure backend server is running on same WiFi network
2. Get backend computer's local IP address:
```bash
   # macOS/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
```
3. Update `BACKEND_URL` with the IP address
4. Rebuild and test:
```bash
   npm run build
   npx cap sync ios
   npx cap open ios
```

---

## 📂 Project Structure
```
keystone-correction-app/
├── src/
│   ├── components/
│   │   ├── CameraScanner.jsx      # Main camera view component
│   │   ├── CameraScanner.css
│   │   ├── Settings.jsx            # Settings page
│   │   ├── Settings.css
│   │   ├── Info.jsx                # Info/help page
│   │   └── Info.css
│   ├── App.jsx                     # Main app with navigation
│   ├── App.css                     # Global styles, results page
│   ├── index.css                   # Critical camera transparency CSS
│   └── main.jsx                    # React entry point
├── ios/                            # iOS native project (Capacitor)
├── android/                        # Android native project (Capacitor)
├── public/                         # Static assets
├── dist/                           # Built web app (generated)
├── capacitor.config.json           # Capacitor configuration
├── vite.config.js                  # Vite build configuration
├── package.json                    # Dependencies
└── README.md
```

---

## 🎨 Customization

### Update App Icon

Replace icons in `ios/App/App/Assets.xcassets/AppIcon.appiconset/`

Recommended: Use https://www.appicon.co/ to generate all sizes from 1024x1024 logo

### Update App Name

**iOS:**
Edit `ios/App/App/Info.plist`:
```xml
<key>CFBundleDisplayName</key>
<string>Your App Name</string>
```

**Android:**
Edit `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Your App Name</string>
```

### Update Colors

TI Red is `#CC0000` throughout the app. To change:
- Search for `#CC0000` in all CSS files
- Replace with your desired color

---

## 🐛 Troubleshooting

### Camera Preview Not Showing

**Issue:** Camera light is on but no preview visible

**Solution:** Make sure `body.camera-running` CSS class is applied and WebView is transparent.

Check in `src/index.css`:
```css
body.camera-running {
  visibility: hidden !important;
  background: transparent !important;
}

.camera-modal {
  visibility: visible !important;
}
```

### CocoaPods Errors (iOS)
```bash
cd ios/App
pod deintegrate
pod cache clean --all
pod install
cd ../..
```

### Xcode Build Errors

1. Clean Build Folder: `Product` → `Clean Build Folder` (Cmd + Shift + K)
2. Delete Derived Data:
```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData
```
3. Rebuild

### Back Button Hidden Behind Notch

Make sure CSS has safe area padding:
```css
.settings-page {
  padding-top: 44px;
}
```

---

## 📱 Distribution (In-House/Testing)

### iOS (Ad Hoc Distribution)

**Option 1: TestFlight (Requires Apple Developer Account - $99/year)**
1. Archive in Xcode: `Product` → `Archive`
2. Upload to App Store Connect
3. Invite testers via email
4. They download from TestFlight app

**Option 2: Ad Hoc Build (Free for up to 100 devices)**
1. Register device UDIDs in Apple Developer Portal
2. Create Ad Hoc provisioning profile
3. Archive and export with Ad Hoc profile
4. Distribute .ipa file via:
   - Email/Dropbox/Google Drive
   - Install using iTunes or Apple Configurator

**Option 3: Direct Install (Development - Easiest)**
1. Connect iPhone via USB
2. Build from Xcode onto device
3. Valid for 7 days (free account) or 1 year (paid account)

### Android (APK Distribution)

**Easiest Method:**
1. Build APK in Android Studio: `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
2. Find APK at: `android/app/build/outputs/apk/debug/app-debug.apk`
3. Share APK file via:
   - Email/Dropbox/Google Drive
   - Slack/Teams
   - USB transfer
4. On Android device:
   - Enable "Install from Unknown Sources" in Settings
   - Open APK file to install

**For Production:**
1. Generate signed APK with release keystore
2. Share the signed APK

---

## 🔒 Security Notes

- Camera permissions are requested at runtime
- No data is stored locally on device
- All image processing happens on backend server
- Images are transmitted as base64 over HTTP (consider HTTPS for production)

---

## 🔄 Development Workflow
```bash
# Make changes to React code
npm run build

# Sync to platforms
npx cap sync ios
npx cap sync android

# Open and run
npx cap open ios
npx cap open android
```

**Hot Reload (Web Testing):**
```bash
npm run dev
# Open http://localhost:5173
# Note: Camera won't work in browser, need physical device
```
