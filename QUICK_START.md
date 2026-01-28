# 🚀 Quick Start Checklist - Week 1

## Monday, January 27, 2026

### Team Meeting (1-2 hours)
- [ ] Review wireframes together
- [ ] Assign screen responsibilities
  - Karrie: Camera integration + iOS
  - Jackson: UI/UX + Android
  - William: Algorithm porting
  - Marc: Backend/optimization
- [ ] Agree on design colors and style
- [ ] Set up team communication (Slack/Discord/Teams)
- [ ] Schedule next check-in

### Individual Tasks

#### Everyone:
- [ ] Install Node.js (v18+)
- [ ] Install React Native CLI: `npm install -g react-native-cli`
- [ ] Clone/download the starter code
- [ ] Run `npm install` in project directory
- [ ] Try running the app on emulator

#### iOS Developers (Karrie):
- [ ] Install Xcode from App Store
- [ ] Run `pod install` in ios folder
- [ ] Test on iOS simulator
- [ ] Test on physical iPhone if available

#### Android Developers (Jackson):
- [ ] Install Android Studio
- [ ] Set up Android SDK
- [ ] Create Android emulator
- [ ] Test on Android emulator
- [ ] Test on physical Android phone if available

#### Algorithm Team (William & Marc):
- [ ] Review current Python code
- [ ] Research opencv.js options
- [ ] Plan algorithm porting strategy
- [ ] Set up Python Flask API for testing

## Tuesday-Wednesday, January 28-29

### Design Work
- [ ] Create high-fidelity mockups in Figma
  - Screen 1: Home
  - Screen 2: Camera
  - Screen 3: Processing
  - Screen 4: Results
- [ ] Export design assets (icons, images)
- [ ] Document color codes and fonts

### Technical Setup
- [ ] Set up Git repository
- [ ] Create development branch
- [ ] Set up version control workflow
- [ ] Install additional dependencies if needed

## Thursday-Friday, January 30-31

### Code Review
- [ ] Walk through starter code as team
- [ ] Understand navigation flow
- [ ] Understand screen structure
- [ ] Identify what needs to be built next

### Week 1 Deliverables
- [ ] Complete wireframes (digital)
- [ ] Style guide document
- [ ] Development environment working
- [ ] App runs on at least one device
- [ ] Team roles assigned
- [ ] Next sprint planned

## Next Week Preview (Week 3-4)

You'll be working on:
1. Refining the UI based on design mockups
2. Adding state management
3. Improving the camera screen
4. Testing on multiple devices
5. Starting algorithm integration

## Common Setup Issues

### Issue: Metro Bundler won't start
**Solution:** 
```bash
npm start -- --reset-cache
```

### Issue: iOS build fails
**Solution:**
```bash
cd ios
pod deintegrate
pod install
cd ..
```

### Issue: Android build fails
**Solution:**
- Check Android SDK is installed
- Check ANDROID_HOME environment variable
- Clean build: `cd android && ./gradlew clean`

### Issue: Camera permission doesn't work
**Solution:**
- iOS: Check Info.plist has camera description
- Android: Check AndroidManifest.xml has permissions
- Restart app after permission changes

## Resources Quick Links

- [React Native Setup](https://reactnative.dev/docs/environment-setup)
- [Troubleshooting Guide](https://reactnative.dev/docs/troubleshooting)
- [React Navigation](https://reactnavigation.org/docs/getting-started)
- [Vision Camera Setup](https://react-native-vision-camera.com/docs/guides)

## Questions to Resolve This Week

1. [ ] React Native vs Flutter vs Native? → Decision: React Native ✅
2. [ ] Backend API vs JavaScript port? → Decision: Start with backend for testing
3. [ ] Which devices for testing? → Decision: [List devices]
4. [ ] Design tool? → Decision: [Figma/Sketch/Adobe XD]
5. [ ] Git workflow? → Decision: [Branch strategy]

## Success Criteria for Week 1

By Friday, February 2:
- ✅ Everyone can run the app
- ✅ Wireframes are complete and approved
- ✅ Design system is documented
- ✅ Roles are assigned
- ✅ Git repository is set up
- ✅ Next 2 weeks are planned

## Team Contacts

- Karrie: [email/phone]
- William: [email/phone]
- Marc: [email/phone]
- Jackson: [email/phone]
- Sponsor: Vincent Tarzi [email]

---

**Remember:** This is Week 1 of 14. Focus on getting the foundation right!
