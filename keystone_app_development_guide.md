# Keystone Correction Mobile App - Development Guide
## Second Semester Plan

### Week 1-2: Planning & Wireframes (Jan 20 - Feb 2)

#### Decision 1: Choose Your Platform
**Recommendation: React Native**
- ✅ Single codebase for iOS & Android
- ✅ Good camera library support (react-native-vision-camera)
- ✅ Can integrate OpenCV via react-native-opencv3 or opencv4nodejs
- ✅ Faster development than native
- ✅ Large community and resources

**Alternative: Native Development**
- iOS: Swift + AVFoundation
- Android: Kotlin + CameraX
- More work but better performance

#### Decision 2: Algorithm Integration Strategy

**Option A: Port Python to JavaScript**
- Rewrite corner detection in JavaScript using opencv.js
- Pros: Everything runs in one environment
- Cons: Need to rewrite tested code

**Option B: Use Python Backend**
- Keep Python algorithm, expose via REST API
- Mobile app sends image → Python server → returns corners
- Pros: Reuse existing code
- Cons: Requires server, network dependency

**Option C: Hybrid - Native Module**
- Wrap Python/OpenCV as React Native native module
- Pros: Reuse code, runs on device
- Cons: More complex setup

**Recommendation: Start with Option B (Python backend) for testing, then move to Option A for production**

---

## Setup Instructions

### 1. Development Environment Setup

#### For React Native:
```bash
# Install Node.js (v18 or later)
# Install React Native CLI
npm install -g react-native-cli

# Initialize project
npx react-native init KeystoneCorrection
cd KeystoneCorrection

# Install dependencies
npm install react-native-vision-camera
npm install @react-native-community/slider
npm install react-native-svg
npm install axios # for API calls
```

#### iOS Specific:
```bash
cd ios
pod install
cd ..
```

#### Android Specific:
- Update `android/app/src/main/AndroidManifest.xml` to add camera permissions

### 2. Camera Integration Libraries

**iOS (AVFoundation via React Native):**
```javascript
import { Camera, useCameraDevices } from 'react-native-vision-camera';
```

**Android (CameraX via React Native):**
Same library works for both platforms

### 3. OpenCV Integration

**Option 1: opencv.js in React Native**
```bash
npm install opencv-react-native
```

**Option 2: Python Backend (for initial testing)**
```python
# Flask API example
from flask import Flask, request, jsonify
import cv2
import numpy as np
# ... your existing code ...

app = Flask(__name__)

@app.route('/detect_corners', methods=['POST'])
def detect_corners():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    # Run your existing corner detection algorithm
    corners = your_corner_detection_function(img)
    return jsonify({'corners': corners.tolist()})
```

---

## App Architecture

### Screen Flow
```
Splash Screen
    ↓
Onboarding (First Time Only)
    ↓
Home Screen
    ↓
Camera Capture Screen → [Guide Overlay]
    ↓
Processing Screen [Loading Indicator]
    ↓
Results Screen [Before/After Comparison]
    ↓
Export/Apply Correction
```

### File Structure
```
KeystoneCorrection/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js
│   │   ├── CameraScreen.js
│   │   ├── ProcessingScreen.js
│   │   ├── ResultsScreen.js
│   │   └── OnboardingScreen.js
│   ├── components/
│   │   ├── CameraOverlay.js      # Grid/guides for alignment
│   │   ├── CornerMarker.js       # Visual corner indicators
│   │   ├── LoadingSpinner.js
│   │   └── BeforeAfterSlider.js
│   ├── utils/
│   │   ├── cornerDetection.js    # Port your algorithm here
│   │   ├── homography.js
│   │   └── imageProcessing.js
│   ├── api/
│   │   └── keystoneAPI.js        # If using backend
│   └── navigation/
│       └── AppNavigator.js
```

---

## Week-by-Week Development Plan

### Week 1-2 (Jan 20 - Feb 2): Planning & Wireframes ✓
**Tasks:**
- [x] Choose platform (React Native recommended)
- [ ] Create wireframes for all 5 screens
- [ ] Design onboarding flow
- [ ] Set up color scheme and typography
- [ ] Create design mockups in Figma/Sketch

**Deliverables:**
- Wireframe document showing all screen flows
- Style guide (colors, fonts, spacing)
- Design mockups

### Week 3-4 (Feb 3 - Feb 16): App Skeleton
**Tasks:**
- [ ] Initialize React Native project
- [ ] Set up navigation between screens
- [ ] Create placeholder screens with basic layout
- [ ] Implement consistent styling across app
- [ ] Set up state management (Context API or Redux)

**Code Example - Navigation Setup:**
```javascript
// AppNavigator.js
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Camera" component={CameraScreen} />
        <Stack.Screen name="Results" component={ResultsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Week 5-6 (Feb 17 - Mar 2): Camera Integration
**Tasks:**
- [ ] Implement camera permissions
- [ ] Create live camera preview
- [ ] Add capture button with feedback
- [ ] Implement grid overlay for alignment
- [ ] Handle image quality (resolution, focus)

**Code Example - Camera Screen:**
```javascript
import { Camera } from 'react-native-vision-camera';

function CameraScreen() {
  const devices = useCameraDevices();
  const device = devices.back;
  
  const takePicture = async () => {
    const photo = await camera.current.takePhoto({
      qualityPrioritization: 'quality',
    });
    // Navigate to processing screen
    navigation.navigate('Processing', { imageUri: photo.path });
  };

  return (
    <View>
      <Camera
        ref={camera}
        device={device}
        isActive={true}
        photo={true}
      />
      <CameraOverlay /> {/* Grid/guides */}
      <CaptureButton onPress={takePicture} />
    </View>
  );
}
```

### Week 7-8 (Mar 3 - Mar 16): Algorithm Integration
**Tasks:**
- [ ] Port corner detection to JavaScript OR set up Python backend
- [ ] Implement homography calculation
- [ ] Create processing screen with progress indicator
- [ ] Display before/after comparison
- [ ] Handle error cases (no corners detected)

**Code Example - Corner Detection Integration:**
```javascript
// If using backend
async function detectCorners(imageUri) {
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'projection.jpg',
  });

  const response = await fetch('http://your-api.com/detect_corners', {
    method: 'POST',
    body: formData,
  });

  return await response.json();
}
```

### Week 9-10 (Mar 17 - Mar 30): User Guidance
**Tasks:**
- [ ] Add real-time guidance prompts ("Move closer", "Tilt up")
- [ ] Implement corner markers that update in real-time
- [ ] Create tutorial/walkthrough for first-time users
- [ ] Add retake functionality
- [ ] Improve error messages

**Guidance Features:**
```javascript
function CameraGuidance({ corners }) {
  const guidance = analyzeImageQuality(corners);
  
  return (
    <View style={styles.guidanceOverlay}>
      {guidance.tooFar && <Text>Move closer to projection</Text>}
      {guidance.tilted && <Text>Keep phone level</Text>}
      {corners.detected && <CornerMarkers corners={corners} />}
    </View>
  );
}
```

### Week 11-12 (Mar 31 - Apr 13): Testing & Iteration
**Tasks:**
- [ ] Test on multiple device sizes
- [ ] Test on different OS versions
- [ ] Optimize performance (image processing speed)
- [ ] Fix layout issues
- [ ] Improve error handling

### Week 13-14 (Apr 14 - Apr 27): Polish & Features
**Tasks:**
- [ ] Refine UI/UX based on testing
- [ ] Add settings screen
- [ ] Implement Help/FAQ section
- [ ] Add analytics (optional)
- [ ] Final bug fixes

---

## Key Technical Considerations

### 1. Camera Permissions
**iOS (Info.plist):**
```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to capture projector output for correction</string>
```

**Android (AndroidManifest.xml):**
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

### 2. Image Quality Guidelines
- Minimum resolution: 1920x1080
- Avoid zoom < 1x (as noted in your document)
- Ensure good lighting
- Keep phone steady (use gyroscope for stability detection)

### 3. Performance Optimization
- Downscale images before processing (as noted in your risk mitigation)
- Use worker threads for heavy computation
- Cache results when possible
- Lazy load non-critical features

### 4. Privacy & Security (Constraint 8)
- Process images in memory only
- Don't store images unless user opts in
- If storing: encrypt at rest using device keychain
- Clear temporary files after processing
- Add privacy policy screen

---

## Testing Strategy

### Device Testing Matrix
| Device Type | iOS | Android |
|-------------|-----|---------|
| Small Phone | iPhone SE | Pixel 4a |
| Standard | iPhone 13 | Samsung S21 |
| Large | iPhone 14 Pro Max | Samsung S22 Ultra |

### Test Scenarios
1. Perfect alignment (control)
2. Vertical distortion
3. Horizontal distortion
4. Tilt distortion
5. Low light conditions
6. High contrast walls
7. Textured walls
8. Dark colored walls

---

## Resources

### React Native
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/)
- [React Native Vision Camera](https://github.com/mrousavy/react-native-vision-camera)

### OpenCV
- [OpenCV.js](https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html)
- [OpenCV Python to JS conversion guide](https://docs.opencv.org/4.x/d0/d84/tutorial_js_usage.html)

### UI/UX
- [Material Design](https://material.io/)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

---

## Next Immediate Steps (This Week)

1. **Install Development Environment**
   - Install Node.js, React Native CLI
   - Set up Android Studio / Xcode
   - Create new React Native project

2. **Create Wireframes**
   - Sketch all 5 screens
   - Define user flow
   - Get team approval

3. **Set Up Version Control**
   - Initialize Git repository
   - Create development branch
   - Set up team collaboration workflow

4. **Team Meeting**
   - Assign screen responsibilities
   - Agree on design system
   - Set up communication channels

---

## Questions to Answer This Week

1. Will you use React Native, Flutter, or Native?
2. Will you port the algorithm to JavaScript or use a backend?
3. What design tool will you use for wireframes? (Figma, Sketch, Adobe XD)
4. How will you handle testing? (Real devices vs emulators)
5. Who is responsible for iOS vs Android specifics?

---

## Risk Mitigation (From Your Document)

**Design Workshop → Complete by Jan 27**
- Hold 2-hour session to agree on app flow
- Use low-fidelity sketches
- Document decisions

**Style Guide → Complete by Feb 2**
- Colors, typography, spacing
- Decide on component library (if any)

**Cross-Platform Testing → Start Feb 3**
- Set up emulators early
- Identify 2-3 physical test devices per platform

---

## Success Criteria

By end of Week 2 (Feb 2), you should have:
- ✅ Platform decision made and documented
- ✅ Complete wireframes for all screens
- ✅ Style guide created
- ✅ Development environment set up
- ✅ Initial project created and running on emulator

This positions you perfectly for Week 3-4 where you'll build the app skeleton.
