/**
 * Processing Screen
 * Shows progress while detecting corners and calculating correction
 */

import React, {useEffect, useState} from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

const ProcessingScreen = ({route, navigation}) => {
  const {imageUri} = route.params;
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Analyzing image...');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Process image using FastAPI backend
    const processImage = async () => {
      try {
        // Step 1: Analyzing image
        setStatusText('Analyzing image...');
        setProgress(20);
        await delay(500);

        // Step 2: Detecting corners
        setStatusText('Detecting corners...');
        setProgress(40);
        
        // Import API function
        const {detectCorners} = require('../api/keystoneAPI');
        
        // Call actual API
        const result = await detectCorners(imageUri);
        
        // Step 3: Calculating correction
        setStatusText('Calculating correction...');
        setProgress(70);
        await delay(500);

        // Step 4: Optimizing parameters
        setStatusText('Optimizing parameters...');
        setProgress(90);
        await delay(500);

        // Step 5: Complete
        setStatusText('Complete!');
        setProgress(100);
        await delay(300);

        // Navigate to results
        navigation.replace('Results', {
          imageUri,
          corners: result,
        });
      } catch (err) {
        console.error('Processing error:', err);
        setError(err.message || 'Failed to process image');
      }
    };

    processImage();
  }, [imageUri, navigation]);

  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

  const handleRetry = () => {
    navigation.goBack();
  };

  const handleManualSelection = () => {
    Alert.alert(
      'Manual Selection',
      'This feature will allow you to manually select corners. Coming soon!',
    );
  };

  if (error) {
    return (
      <View style={styles.container}>
        <Icon name="error-outline" size={80} color="#F44336" />
        <Text style={styles.errorTitle}>Unable to Detect Corners</Text>
        <Text style={styles.errorMessage}>
          Make sure:{'\n'}
          • All 4 corners are visible{'\n'}
          • Image is well-lit{'\n'}
          • Projection is clearly visible
        </Text>
        <TouchableOpacity style={styles.retryButton} onPress={handleRetry}>
          <Icon name="refresh" size={24} color="#fff" />
          <Text style={styles.retryButtonText}>Try Again</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.manualButton}
          onPress={handleManualSelection}>
          <Icon name="touch-app" size={24} color="#2196F3" />
          <Text style={styles.manualButtonText}>Manual Selection</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Image Thumbnail */}
      <View style={styles.imageContainer}>
        <Image source={{uri: `file://${imageUri}`}} style={styles.image} />
      </View>

      {/* Processing Status */}
      <Text style={styles.title}>Processing Image...</Text>

      {/* Progress Bar */}
      <View style={styles.progressBarContainer}>
        <View style={[styles.progressBar, {width: `${progress}%`}]} />
      </View>
      <Text style={styles.progressText}>{progress}%</Text>

      {/* Status Text */}
      <Text style={styles.statusText}>{statusText}</Text>

      {/* Activity Indicator */}
      <ActivityIndicator size="large" color="#2196F3" style={styles.spinner} />

      {/* Cancel Button (optional) */}
      <TouchableOpacity
        style={styles.cancelButton}
        onPress={() => navigation.goBack()}>
        <Text style={styles.cancelButtonText}>Cancel</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  imageContainer: {
    width: 200,
    height: 200,
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 30,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 20,
  },
  progressBarContainer: {
    width: '80%',
    height: 8,
    backgroundColor: '#E0E0E0',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#2196F3',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 16,
    color: '#757575',
    marginBottom: 20,
  },
  statusText: {
    fontSize: 16,
    color: '#2196F3',
    marginBottom: 20,
  },
  spinner: {
    marginVertical: 20,
  },
  cancelButton: {
    marginTop: 20,
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  cancelButtonText: {
    fontSize: 16,
    color: '#757575',
  },
  // Error styles
  errorTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#212121',
    marginTop: 20,
    marginBottom: 12,
  },
  errorMessage: {
    fontSize: 16,
    color: '#757575',
    textAlign: 'center',
    marginBottom: 30,
    lineHeight: 24,
  },
  retryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2196F3',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    marginBottom: 12,
  },
  retryButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginLeft: 8,
  },
  manualButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#2196F3',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  manualButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2196F3',
    marginLeft: 8,
  },
});

export default ProcessingScreen;
