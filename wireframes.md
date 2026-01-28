# Keystone Correction App - Wireframe Templates

## Screen 1: Home Screen

```
┌─────────────────────────────────────┐
│  ☰                          [?]     │ <- Menu, Help
│                                     │
│         Keystone Correction         │
│                                     │
│      ┌───────────────────────┐     │
│      │                       │     │
│      │    📱 → 📽️ → ☑️      │     │
│      │                       │     │
│      │   Simple. Automatic.  │     │
│      │    Correction.        │     │
│      └───────────────────────┘     │
│                                     │
│                                     │
│      ┌───────────────────────┐     │
│      │   📷 Start Camera     │     │ <- Primary CTA
│      └───────────────────────┘     │
│                                     │
│      ┌───────────────────────┐     │
│      │   📂 Choose Image     │     │ <- Secondary option
│      └───────────────────────┘     │
│                                     │
│                                     │
│   Recent Corrections:               │
│   • Living Room - 2 hours ago       │
│   • Bedroom - Yesterday             │
│                                     │
└─────────────────────────────────────┘
```

**Key Elements:**
- App branding/logo
- Quick start button (Camera)
- Alternative: Upload existing photo
- Recent corrections history
- Help/Info access

---

## Screen 2: Onboarding (First Time Only)

```
┌─────────────────────────────────────┐
│              Step 1/3               │ <- Progress indicator
│                                     │
│      ┌───────────────────────┐     │
│      │                       │     │
│      │    [Illustration]     │     │
│      │    Projector with     │     │
│      │    distorted output   │     │
│      │                       │     │
│      └───────────────────────┘     │
│                                     │
│   Fix Distorted Projections         │
│                                     │
│   Automatically correct keystone    │
│   distortion with just your phone   │
│   camera. No extra hardware needed. │
│                                     │
│                                     │
│                                     │
│   ●  ○  ○                          │ <- Page indicators
│                                     │
│   [Skip]              [Next →]      │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│              Step 2/3               │
│                                     │
│      ┌───────────────────────┐     │
│      │                       │     │
│      │    [Illustration]     │     │
│      │    Phone taking       │     │
│      │    photo of screen    │     │
│      │                       │     │
│      └───────────────────────┘     │
│                                     │
│   How It Works                      │
│                                     │
│   1. Point your camera at the       │
│      projection                     │
│   2. Follow the on-screen guides    │
│   3. Capture the image              │
│   4. Get correction parameters      │
│                                     │
│   ○  ●  ○                          │
│                                     │
│   [Skip]              [Next →]      │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│              Step 3/3               │
│                                     │
│      ┌───────────────────────┐     │
│      │                       │     │
│      │    [Illustration]     │     │
│      │    Corrected screen   │     │
│      │    with checkmark     │     │
│      │                       │     │
│      └───────────────────────┘     │
│                                     │
│   Best Results Tips                 │
│                                     │
│   ✓ Use good lighting               │
│   ✓ Capture from straight on        │
│   ✓ Include all four corners        │
│   ✓ Avoid zoom (keep at 1.0x)       │
│                                     │
│                                     │
│   ○  ○  ●                          │
│                                     │
│   [Skip]         [Get Started]      │
│                                     │
└─────────────────────────────────────┘
```

---

## Screen 3: Camera Capture Screen

```
┌─────────────────────────────────────┐
│  ← Back              🔦 Flash  ⚙️   │ <- Nav + controls
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │  ┌─┐                   ┌─┐  │   │ <- Corner markers
│  │  └─┘    CAMERA VIEW    └─┘  │   │    (show when detected)
│  │                             │   │
│  │                             │   │
│  │         [ GRID ]            │   │ <- Alignment grid
│  │                             │   │
│  │                             │   │
│  │  ┌─┐                   ┌─┐  │   │
│  │  └─┘                   └─┘  │   │
│  └─────────────────────────────┘   │
│                                     │
│  💡 Tip: Center the projection     │ <- Guidance text
│     in the viewfinder               │    (dynamic)
│                                     │
│  ┌─────┐       ⭕        ┌─────┐   │
│  │ 📂  │                 │ 🔄  │   │
│  └─────┘                 └─────┘   │
│  Gallery    Capture      Flip Cam  │
│                                     │
└─────────────────────────────────────┘
```

**States:**
1. Initial: Grid shown, guidance text
2. Corners Detected: Green corner markers appear
3. Good Alignment: Checkmark, "Ready to capture"
4. Poor Alignment: Warning, "Move closer" or "Tilt up"

**Dynamic Guidance Examples:**
- "Move closer to the projection"
- "Tilt phone slightly upward"
- "Keep phone level"
- "✓ Good alignment - ready to capture"
- "Include all four corners"

---

## Screen 4: Processing Screen

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│      ┌───────────────────────┐     │
│      │                       │     │
│      │    [Thumbnail of      │     │
│      │     captured image]   │     │
│      │                       │     │
│      └───────────────────────┘     │
│                                     │
│          Processing Image...        │
│                                     │
│         ◉◉◉◉◉◉◉◉◉◯◯◯            │ <- Progress bar
│                                     │
│         Detecting corners...        │ <- Status text
│                                     │
│                                     │
│            [Cancel]                 │ <- Optional
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Processing Steps (shown sequentially):**
1. "Analyzing image..."
2. "Detecting corners..."
3. "Calculating correction..."
4. "Optimizing parameters..."
5. "Complete!"

**Error State:**
```
┌─────────────────────────────────────┐
│                                     │
│         ⚠️                          │
│                                     │
│    Unable to Detect Corners         │
│                                     │
│  Make sure:                         │
│  • All 4 corners are visible        │
│  • Image is well-lit                │
│  • Projection is clearly visible    │
│                                     │
│      ┌───────────────────────┐     │
│      │   Try Again           │     │
│      └───────────────────────┘     │
│                                     │
│      ┌───────────────────────┐     │
│      │   Manual Selection    │     │ <- Fallback option
│      └───────────────────────┘     │
│                                     │
└─────────────────────────────────────┘
```

---

## Screen 5: Results Screen

```
┌─────────────────────────────────────┐
│  ← Back                    [Share]  │
│                                     │
│        Correction Complete! ✓       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │   BEFORE      ◀─────▶       │   │ <- Slider to compare
│  │                      AFTER   │   │
│  │   [Image split view]        │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  📏 Correction Parameters:          │
│  ┌─────────────────────────────┐   │
│  │ Top Left:     (120, 45)     │   │
│  │ Top Right:    (3710, 52)    │   │
│  │ Bottom Right: (3698, 2103)  │   │
│  │ Bottom Left:  (132, 2096)   │   │
│  └─────────────────────────────┘   │
│                                     │
│      ┌───────────────────────┐     │
│      │  📋 Copy Parameters   │     │ <- Primary action
│      └───────────────────────┘     │
│                                     │
│      ┌───────────────────────┐     │
│      │  💾 Save Result       │     │
│      └───────────────────────┘     │
│                                     │
│      Apply to Another  →            │
│                                     │
└─────────────────────────────────────┘
```

**Interactive Elements:**
- Before/After slider (swipe left/right)
- Copy parameters to clipboard
- Save corrected image
- Share functionality
- "Apply to Another" → returns to camera

**Alternative: Side-by-side view**
```
│  ┌──────────┐  ┌──────────┐  │
│  │  BEFORE  │  │  AFTER   │  │
│  │          │  │          │  │
│  │  [Image] │  │  [Image] │  │
│  │          │  │          │  │
│  └──────────┘  └──────────┘  │
```

---

## Screen 6: Settings Screen (Optional)

```
┌─────────────────────────────────────┐
│  ← Settings                         │
│                                     │
│  Camera                             │
│  ┌─────────────────────────────┐   │
│  │ Grid Overlay         [ON] ○ │   │
│  │ Corner Markers       [ON] ○ │   │
│  │ Auto Flash          [OFF] ○ │   │
│  │ Image Quality         High  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Correction                         │
│  ┌─────────────────────────────┐   │
│  │ Sensitivity        Medium ▼ │   │
│  │ Auto-process        [ON] ○  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Storage                            │
│  ┌─────────────────────────────┐   │
│  │ Save History        [ON] ○  │   │
│  │ Auto-save Images   [OFF] ○  │   │
│  │ Clear History             → │   │
│  └─────────────────────────────┘   │
│                                     │
│  About                              │
│  ┌─────────────────────────────┐   │
│  │ Version 1.0.0               │   │
│  │ Help & FAQ                → │   │
│  │ Privacy Policy            → │   │
│  │ Terms of Service          → │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

---

## Screen 7: Help/FAQ Screen (Optional)

```
┌─────────────────────────────────────┐
│  ← Help & FAQ                       │
│                                     │
│  Getting Started                    │
│  ▼ How do I use this app?           │
│    1. Point camera at projection    │
│    2. Align within guides           │
│    3. Capture image                 │
│    4. Get correction parameters     │
│                                     │
│  Troubleshooting                    │
│  ▶ Corners not detected             │
│  ▶ Results not accurate             │
│  ▶ App crashes                      │
│  ▶ Camera not working               │
│                                     │
│  Best Practices                     │
│  ▶ Lighting conditions              │
│  ▶ Camera positioning               │
│  ▶ Supported wall types             │
│                                     │
│  Advanced                           │
│  ▶ Manual corner selection          │
│  ▶ Sensitivity settings             │
│  ▶ Export options                   │
│                                     │
│  Contact Support                    │
│  📧 support@example.com             │
│                                     │
└─────────────────────────────────────┘
```

---

## Navigation Flow Diagram

```
      ┌──────────────┐
      │   Splash     │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │  Onboarding  │ (First time only)
      │  (3 screens) │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
  ┌───│     Home     │───┐
  │   └──────┬───────┘   │
  │          │           │
  │          ▼           │
  │   ┌──────────────┐   │
  │   │    Camera    │   │
  │   └──────┬───────┘   │
  │          │           │
  │          ▼           │
  │   ┌──────────────┐   │
  │   │  Processing  │   │
  │   └──────┬───────┘   │
  │          │           │
  │          ▼           │
  │   ┌──────────────┐   │
  └──▶│   Results    │◀──┘
      └──────┬───────┘
             │
      ┌──────┴────────┬──────────┐
      │               │          │
      ▼               ▼          ▼
 ┌─────────┐   ┌──────────┐  ┌───────┐
 │Settings │   │   Help   │  │ Share │
 └─────────┘   └──────────┘  └───────┘
```

---

## Component Library

### Buttons
```
Primary:   ┌───────────────────────┐
           │   Action Button       │  <- Blue, bold
           └───────────────────────┘

Secondary: ┌───────────────────────┐
           │   Action Button       │  <- Gray outline
           └───────────────────────┘

Icon:      [ 📷 ]  [ ⚙️ ]  [ ? ]
```

### Input Fields
```
┌─────────────────────────────────┐
│ Label                           │
│ ┌─────────────────────────────┐ │
│ │ Placeholder text            │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

### Cards
```
┌─────────────────────────────────┐
│ Title                           │
│ ────────────────────────────── │
│                                 │
│ Content goes here               │
│                                 │
└─────────────────────────────────┘
```

### Alerts
```
┌─────────────────────────────────┐
│ ⚠️  Warning                     │
│                                 │
│ Description of the warning      │
│                                 │
│         [ OK ]  [ Cancel ]      │
└─────────────────────────────────┘
```

---

## Design Specifications

### Colors (Recommended Palette)
```
Primary:    #2196F3  (Blue)       [■■■■■]
Secondary:  #FFC107  (Amber)      [■■■■■]
Success:    #4CAF50  (Green)      [■■■■■]
Error:      #F44336  (Red)        [■■■■■]
Warning:    #FF9800  (Orange)     [■■■■■]
Text:       #212121  (Dark Gray)  [■■■■■]
Background: #FFFFFF  (White)      [□□□□□]
Divider:    #BDBDBD  (Gray)       [■■■■■]
```

### Typography
```
Heading 1:  24px, Bold
Heading 2:  20px, Bold
Heading 3:  18px, Semi-Bold
Body:       16px, Regular
Caption:    14px, Regular
Button:     16px, Bold
```

### Spacing
```
Tiny:    4px
Small:   8px
Medium:  16px
Large:   24px
XLarge:  32px
```

### Icons
- Use consistent icon library (Material Icons or SF Symbols)
- Size: 24x24px for toolbar, 48x48px for features
- Color: Match text color or brand color

---

## Interaction States

### Button States
```
Normal:    ┌───────────┐
           │  Button   │
           └───────────┘

Pressed:   ┌───────────┐
           │  Button   │  <- Darker/Raised
           └───────────┘

Disabled:  ┌───────────┐
           │  Button   │  <- Gray/Faded
           └───────────┘

Loading:   ┌───────────┐
           │  ◉◉◉◉◉   │  <- Spinner
           └───────────┘
```

### Camera Guidance States
```
Searching:     "Searching for projection..."
                [Yellow indicator]

Found:         "Projection detected"
                [Green corner markers]

Too Far:       "Move closer"
                [Red indicator]

Good:          "✓ Ready to capture"
                [Green checkmark]
```

---

## Responsive Considerations

### Small Screens (iPhone SE, small Android)
- Larger buttons (min 44x44px touch targets)
- Simplified layouts
- Fewer elements per screen

### Large Screens (Plus/Max models)
- Utilize extra space for larger preview
- Show more guidance text
- Side-by-side comparisons

### Tablets (if supporting)
- Two-column layouts where appropriate
- Larger imagery
- More detailed instructions

---

## Next Steps

1. **Review & Approve**
   - Team review of wireframes
   - Sponsor feedback
   - User testing with sketches

2. **High-Fidelity Mockups**
   - Create in Figma/Sketch/Adobe XD
   - Apply color scheme
   - Add real imagery

3. **Prototype**
   - Create clickable prototype
   - Test navigation flow
   - Validate interactions

4. **Development Handoff**
   - Export assets
   - Document specifications
   - Begin implementation

