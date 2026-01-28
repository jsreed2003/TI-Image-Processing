# Keystone Correction Mobile App

Automatic keystone correction app for DLP projectors using computer vision and mobile device cameras.

## 🎯 Project Overview

This React Native application helps users automatically correct keystone distortion in projector outputs by:
1. Capturing an image of the projector output using the phone camera
2. Detecting the four corners of the projection
3. Computing optimal correction parameters
4. Displaying before/after results with correction values

**Target Platform:** iOS and Android  
**Development Timeline:** Spring 2026 Semester  
**Sponsor:** Texas Instruments (DLP Projectors)

## 📱 Features

### Current Implementation
- ✅ Home screen with navigation
- ✅ Camera integration with live preview
- ✅ Alignment grid overlay
- ✅ Processing screen with progress indicator
- ✅ Results screen with before/after comparison
- ✅ Parameter display and copy functionality
- ✅ Basic onboarding flow

### Coming Soon (Weeks 5-14)
- 🔄 Real-time corner detection
- 🔄 Dynamic camera guidance ("Move closer", "Tilt up")
- 🔄 Integration with Python/OpenCV algorithm
- 🔄 Manual corner selection fallback
- 🔄 Settings screen (sensitivity, auto-save, etc.)
- 🔄 Help/FAQ content
- 🔄 Image quality optimization
- 🔄 Performance improvements

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or later)
- **npm** or **yarn**
- **React Native CLI**
- **Xcode** (for iOS development on Mac)
- **Android Studio** (for Android development)

### Installation

1. **Clone or download this starter project**

2. **Install dependencies**
```bash
cd keystone-app-starter
npm install
```

3. **iOS Setup** (Mac only)
```bash
cd ios
pod install
cd ..
```

4. **Android Setup**
- Open Android Studio
- Open the `android` folder
- Let Gradle sync
- Update SDK if needed

### Running the App

**iOS:**
```bash
npm run ios
# or
npx react-native run-ios
```

**Android:**
```bash
npm run android
# or
npx react-native run-android
```

**Start Metro Bundler:**
```bash
npm start
```

## 📂 Project Structure

```
keystone-app-starter/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js          # Landing screen
│   │   ├── CameraScreen.js        # Camera capture with guides
│   │   ├── ProcessingScreen.js    # Processing with progress
│   │   ├── ResultsScreen.js       # Results display
│   │   └── OnboardingScreen.js    # First-time user flow
│   ├── components/                # Reusable components (TODO)
│   ├── utils/                     # Helper functions (TODO)
│   └── api/                       # API calls (TODO)
├── App.js                         # Main app component
├── package.json
└── README.md
```

## 🔧 Key Technologies

- **React Native** - Cross-platform mobile framework
- **React Navigation** - Screen navigation
- **react-native-vision-camera** - Camera integration
- **OpenCV** - Computer vision (to be integrated)
- **Python** - Backend algorithm (optional)

## 🎨 Design System

### Colors
- Primary: `#2196F3` (Blue)
- Success: `#4CAF50` (Green)
- Error: `#F44336` (Red)
- Text: `#212121` (Dark Gray)
- Background: `#FFFFFF` (White)

### Typography
- Heading: 24px, Bold
- Body: 16px, Regular
- Button: 16px, Bold

## 📋 Development Roadmap

### ✅ Week 1-2 (Jan 20 - Feb 2): Planning & Setup
- [x] Choose platform (React Native)
- [x] Create wireframes
- [x] Set up project structure
- [x] Basic navigation
- [ ] Design mockups in Figma

### 🔄 Week 3-4 (Feb 3 - Feb 16): App Skeleton
- [ ] Refine all screens
- [ ] Add state management
- [ ] Implement consistent styling
- [ ] Add loading states

### 📅 Week 5-6 (Feb 17 - Mar 2): Camera Integration
- [ ] Improve camera permissions flow
- [ ] Add real-time guidance
- [ ] Implement corner detection preview
- [ ] Handle various lighting conditions

### 📅 Week 7-8 (Mar 3 - Mar 16): Algorithm Integration
- [ ] Integrate Python backend OR
- [ ] Port algorithm to JavaScript
- [ ] Connect processing to real CV
- [ ] Handle error cases

### 📅 Week 9-10 (Mar 17 - Mar 30): User Guidance
- [ ] Add AR overlays
- [ ] Implement real-time feedback
- [ ] Create tutorial walkthrough
- [ ] Improve error messages

### 📅 Week 11-12 (Mar 31 - Apr 13): Testing
- [ ] Test on multiple devices
- [ ] Performance optimization
- [ ] Fix bugs
- [ ] User testing

### 📅 Week 13-14 (Apr 14 - Apr 27): Polish
- [ ] Refine UI/UX
- [ ] Add analytics (optional)
- [ ] Complete help content
- [ ] Final bug fixes

## 🔌 Algorithm Integration Options

### Option A: Python Backend (Recommended for Testing)
1. Run your existing Python code as a Flask API
2. Mobile app sends image → Python processes → returns corners
3. Pros: Reuse existing code, faster development
4. Cons: Requires server/network

**Example API:**
```python
from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/detect_corners', methods=['POST'])
def detect_corners():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    # Your existing corner detection code here
    corners = your_corner_detection_function(img)
    return jsonify({
        'originalCorners': corners.tolist(),
        'optimalCorners': optimal_corners.tolist()
    })
```

### Option B: JavaScript/OpenCV.js (For Production)
1. Port Python algorithm to JavaScript
2. Use opencv.js or react-native-opencv
3. Pros: Everything runs on-device, no network needed
4. Cons: Need to rewrite tested code

### Option C: Native Module (Advanced)
1. Wrap Python/C++ as React Native module
2. Best performance
3. Most complex setup

## 🧪 Testing

### Manual Testing Checklist
- [ ] Camera permissions work on iOS and Android
- [ ] Image capture quality is good
- [ ] Processing shows progress correctly
- [ ] Results display parameters accurately
- [ ] Copy to clipboard works
- [ ] Navigation flows smoothly
- [ ] App handles errors gracefully

### Device Testing
Test on at least:
- iPhone (iOS 15+)
- Android phone (Android 10+)
- Different screen sizes

## 🐛 Known Issues & TODOs

1. **Camera Screen**
   - [ ] Corner detection is simulated (not real)
   - [ ] Flash doesn't work properly
   - [ ] Gallery picker not implemented
   - [ ] Camera flip not implemented

2. **Processing Screen**
   - [ ] Progress is simulated (not real)
   - [ ] Need to integrate actual CV algorithm
   - [ ] Manual corner selection not implemented

3. **Results Screen**
   - [ ] Before/After comparison needs real images
   - [ ] Save functionality not implemented
   - [ ] Share could be improved

4. **General**
   - [ ] Settings screen is placeholder
   - [ ] Help content needs to be written
   - [ ] Onboarding needs full 3-screen flow
   - [ ] No state persistence (history)
   - [ ] No analytics

## 📱 Permissions Required

### iOS (Info.plist)
```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to capture projector output</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We need photo library access to save correction results</string>
```

### Android (AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

## 🔒 Privacy & Security

- Images are processed in memory only (no storage by default)
- User can opt-in to save results
- No cloud upload (all processing on-device)
- Complies with FIPS requirements
- Works in restricted regions (China)

## 🤝 Team Responsibilities

- **Karrie:** Camera integration, AR features, iOS testing
- **Jackson:** UI/UX design, presentations, Android testing
- **William:** Corner detection algorithm, JavaScript port
- **Marc:** Algorithm optimization, performance, testing

## 📚 Resources

- [React Native Docs](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Vision Camera](https://github.com/mrousavy/react-native-vision-camera)
- [OpenCV.js](https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html)
- [Material Design](https://material.io/)
- [iOS HIG](https://developer.apple.com/design/human-interface-guidelines/)

## 🆘 Getting Help

1. Check this README
2. Review the Senior Design Document
3. Check React Native documentation
4. Ask team members
5. Post in team Slack/Discord

## 📄 License

Senior Design Project - Texas Instruments DLP Projectors  
University Project - Spring 2026

---

**Last Updated:** January 26, 2026  
**Version:** 1.0.0 (Starter Code)
