/**
 * Camera Screen
 * Live camera feed with alignment guides and corner detection
 */

import React, {useRef, useState, useEffect} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from 'react-native';
import {Camera, useCameraDevices} from 'react-native-vision-camera';
import Icon from 'react-native-vector-icons/MaterialIcons';

const CameraScreen = ({navigation}) => {
  const camera = useRef(null);
  const devices = useCameraDevices();
  const device = devices.back;

  const [cameraPermission, setCameraPermission] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [flashOn, setFlashOn] = useState(false);
  const [cornersDetected, setCornersDetected] = useState(false);
  const [guidanceText, setGuidanceText] = useState('Center the projection in the viewfinder');

  useEffect(() => {
    // Check camera permissions
    Camera.getCameraPermissionStatus().then(status => {
      setCameraPermission(status);
      if (status !== 'authorized') {
        Camera.requestCameraPermission().then(newStatus => {
          setCameraPermission(newStatus);
        });
      }
    });
  }, []);

  const takePicture = async () => {
    if (!camera.current) return;

    try {
      setIsCapturing(true);
      const photo = await camera.current.takePhoto({
        qualityPrioritization: 'quality',
        flash: flashOn ? 'on' : 'off',
      });

      // Navigate to processing screen with image
      navigation.navigate('Processing', {
        imageUri: photo.path,
      });
    } catch (error) {
      console.error('Error taking picture:', error);
      Alert.alert('Error', 'Failed to capture image. Please try again.');
    } finally {
      setIsCapturing(false);
    }
  };

  // Simulate corner detection (in production, this would use actual CV)
  useEffect(() => {
    const timer = setTimeout(() => {
      setCornersDetected(true);
      setGuidanceText('✓ Good alignment - ready to capture');
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  if (cameraPermission === null) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.permissionText}>Checking camera permissions...</Text>
      </View>
    );
  }

  if (cameraPermission !== 'authorized') {
    return (
      <View style={styles.centerContainer}>
        <Icon name="camera-alt" size={80} color="#BDBDBD" />
        <Text style={styles.permissionText}>Camera permission required</Text>
        <TouchableOpacity
          style={styles.permissionButton}
          onPress={() => Camera.requestCameraPermission()}>
          <Text style={styles.permissionButtonText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.permissionText}>No camera available</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Camera View */}
      <Camera
        ref={camera}
        style={styles.camera}
        device={device}
        isActive={true}
        photo={true}
      />

      {/* Alignment Grid Overlay */}
      <View style={styles.gridOverlay}>
        {/* Vertical lines */}
        <View style={[styles.gridLine, styles.verticalLine, {left: '33%'}]} />
        <View style={[styles.gridLine, styles.verticalLine, {left: '66%'}]} />
        {/* Horizontal lines */}
        <View style={[styles.gridLine, styles.horizontalLine, {top: '33%'}]} />
        <View style={[styles.gridLine, styles.horizontalLine, {top: '66%'}]} />
      </View>

      {/* Corner Markers (shown when corners detected) */}
      {cornersDetected && (
        <View style={styles.cornersOverlay}>
          <View style={[styles.corner, styles.topLeft]} />
          <View style={[styles.corner, styles.topRight]} />
          <View style={[styles.corner, styles.bottomRight]} />
          <View style={[styles.corner, styles.bottomLeft]} />
        </View>
      )}

      {/* Top Controls */}
      <View style={styles.topControls}>
        <TouchableOpacity
          style={styles.iconButton}
          onPress={() => navigation.goBack()}>
          <Icon name="arrow-back" size={28} color="#fff" />
        </TouchableOpacity>

        <View style={styles.topRightControls}>
          <TouchableOpacity
            style={styles.iconButton}
            onPress={() => setFlashOn(!flashOn)}>
            <Icon
              name={flashOn ? 'flash-on' : 'flash-off'}
              size={28}
              color="#fff"
            />
          </TouchableOpacity>
        </View>
      </View>

      {/* Guidance Text */}
      <View style={styles.guidanceContainer}>
        <View
          style={[
            styles.guidanceBubble,
            cornersDetected ? styles.guidanceSuccess : styles.guidanceNeutral,
          ]}>
          <Text style={styles.guidanceText}>{guidanceText}</Text>
        </View>
      </View>

      {/* Bottom Controls */}
      <View style={styles.bottomControls}>
        <TouchableOpacity
          style={styles.sideButton}
          onPress={() => {
            /* TODO: Open gallery */
            Alert.alert('Gallery', 'Image picker coming soon!');
          }}>
          <Icon name="photo-library" size={32} color="#fff" />
          <Text style={styles.sideButtonText}>Gallery</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.captureButton, isCapturing && styles.capturingButton]}
          onPress={takePicture}
          disabled={isCapturing}>
          {isCapturing ? (
            <ActivityIndicator size="large" color="#fff" />
          ) : (
            <View style={styles.captureButtonInner} />
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.sideButton}
          onPress={() => {
            /* TODO: Flip camera */
            Alert.alert('Info', 'Camera flip coming soon!');
          }}>
          <Icon name="flip-camera-ios" size={32} color="#fff" />
          <Text style={styles.sideButtonText}>Flip</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  camera: {
    flex: 1,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 20,
  },
  permissionText: {
    fontSize: 16,
    color: '#757575',
    marginTop: 16,
    textAlign: 'center',
  },
  permissionButton: {
    marginTop: 20,
    backgroundColor: '#2196F3',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  permissionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  gridOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    pointerEvents: 'none',
  },
  gridLine: {
    position: 'absolute',
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
  },
  verticalLine: {
    width: 1,
    height: '100%',
  },
  horizontalLine: {
    height: 1,
    width: '100%',
  },
  cornersOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    pointerEvents: 'none',
  },
  corner: {
    position: 'absolute',
    width: 40,
    height: 40,
    borderColor: '#4CAF50',
    borderWidth: 3,
  },
  topLeft: {
    top: '15%',
    left: '10%',
    borderRightWidth: 0,
    borderBottomWidth: 0,
  },
  topRight: {
    top: '15%',
    right: '10%',
    borderLeftWidth: 0,
    borderBottomWidth: 0,
  },
  bottomRight: {
    bottom: '20%',
    right: '10%',
    borderLeftWidth: 0,
    borderTopWidth: 0,
  },
  bottomLeft: {
    bottom: '20%',
    left: '10%',
    borderRightWidth: 0,
    borderTopWidth: 0,
  },
  topControls: {
    position: 'absolute',
    top: 20,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
  },
  topRightControls: {
    flexDirection: 'row',
  },
  iconButton: {
    padding: 8,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderRadius: 25,
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  guidanceContainer: {
    position: 'absolute',
    top: '45%',
    left: 20,
    right: 20,
    alignItems: 'center',
  },
  guidanceBubble: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 20,
    maxWidth: '80%',
  },
  guidanceNeutral: {
    backgroundColor: 'rgba(33, 150, 243, 0.9)',
  },
  guidanceSuccess: {
    backgroundColor: 'rgba(76, 175, 80, 0.9)',
  },
  guidanceText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  bottomControls: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  sideButton: {
    alignItems: 'center',
  },
  sideButtonText: {
    color: '#fff',
    fontSize: 12,
    marginTop: 4,
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    borderColor: '#fff',
  },
  captureButtonInner: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#fff',
  },
  capturingButton: {
    backgroundColor: 'rgba(33, 150, 243, 0.5)',
  },
});

export default CameraScreen;
