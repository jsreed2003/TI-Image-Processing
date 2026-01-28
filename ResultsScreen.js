/**
 * Results Screen
 * Display correction results with before/after comparison and parameters
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  Clipboard,
  Share,
} from 'react-native';
import Slider from '@react-native-community/slider';
import Icon from 'react-native-vector-icons/MaterialIcons';

const ResultsScreen = ({route, navigation}) => {
  const {imageUri, corners} = route.params;
  const [sliderValue, setSliderValue] = useState(50);

  const {originalCorners, optimalCorners} = corners;

  const formatCorner = (corner, label) => {
    return `${label}: (${Math.round(corner[0])}, ${Math.round(corner[1])})`;
  };

  const copyParameters = () => {
    const params = `Top Left: (${optimalCorners[0][0]}, ${optimalCorners[0][1]})
Top Right: (${optimalCorners[1][0]}, ${optimalCorners[1][1]})
Bottom Right: (${optimalCorners[2][0]}, ${optimalCorners[2][1]})
Bottom Left: (${optimalCorners[3][0]}, ${optimalCorners[3][1]})`;

    Clipboard.setString(params);
    Alert.alert('Copied', 'Parameters copied to clipboard');
  };

  const shareResults = async () => {
    try {
      await Share.share({
        message: `Keystone Correction Parameters:
Top Left: (${optimalCorners[0][0]}, ${optimalCorners[0][1]})
Top Right: (${optimalCorners[1][0]}, ${optimalCorners[1][1]})
Bottom Right: (${optimalCorners[2][0]}, ${optimalCorners[2][1]})
Bottom Left: (${optimalCorners[3][0]}, ${optimalCorners[3][1]})`,
      });
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  const saveResult = () => {
    // TODO: Implement save to device
    Alert.alert('Save', 'Save functionality coming soon!');
  };

  const applyToAnother = () => {
    navigation.navigate('Camera');
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Success Header */}
        <View style={styles.header}>
          <Icon name="check-circle" size={60} color="#4CAF50" />
          <Text style={styles.title}>Correction Complete!</Text>
        </View>

        {/* Before/After Comparison */}
        <View style={styles.comparisonContainer}>
          <Text style={styles.sectionTitle}>Before / After Comparison</Text>
          
          {/* Image Container with Slider Overlay */}
          <View style={styles.imageComparison}>
            {/* After Image (full) */}
            <Image
              source={{uri: `file://${imageUri}`}}
              style={styles.comparisonImage}
            />
            
            {/* Before Image (clipped) */}
            <View
              style={[
                styles.beforeImageContainer,
                {width: `${sliderValue}%`},
              ]}>
              <Image
                source={{uri: `file://${imageUri}`}}
                style={styles.comparisonImage}
              />
            </View>

            {/* Divider Line */}
            <View
              style={[styles.dividerLine, {left: `${sliderValue}%`}]}>
              <View style={styles.dividerHandle} />
            </View>

            {/* Labels */}
            <View style={styles.labelsContainer}>
              <Text style={styles.beforeLabel}>BEFORE</Text>
              <Text style={styles.afterLabel}>AFTER</Text>
            </View>
          </View>

          {/* Slider */}
          <Slider
            style={styles.slider}
            minimumValue={0}
            maximumValue={100}
            value={sliderValue}
            onValueChange={setSliderValue}
            minimumTrackTintColor="#2196F3"
            maximumTrackTintColor="#BDBDBD"
            thumbTintColor="#2196F3"
          />
        </View>

        {/* Correction Parameters */}
        <View style={styles.parametersContainer}>
          <Text style={styles.sectionTitle}>📏 Correction Parameters</Text>
          <View style={styles.parametersBox}>
            <Text style={styles.parameterText}>
              {formatCorner(optimalCorners[0], 'Top Left')}
            </Text>
            <Text style={styles.parameterText}>
              {formatCorner(optimalCorners[1], 'Top Right')}
            </Text>
            <Text style={styles.parameterText}>
              {formatCorner(optimalCorners[2], 'Bottom Right')}
            </Text>
            <Text style={styles.parameterText}>
              {formatCorner(optimalCorners[3], 'Bottom Left')}
            </Text>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionsContainer}>
          <TouchableOpacity
            style={[styles.button, styles.primaryButton]}
            onPress={copyParameters}>
            <Icon name="content-copy" size={24} color="#fff" />
            <Text style={styles.primaryButtonText}>Copy Parameters</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.secondaryButton]}
            onPress={saveResult}>
            <Icon name="save" size={24} color="#2196F3" />
            <Text style={styles.secondaryButtonText}>Save Result</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.secondaryButton]}
            onPress={shareResults}>
            <Icon name="share" size={24} color="#2196F3" />
            <Text style={styles.secondaryButtonText}>Share</Text>
          </TouchableOpacity>
        </View>

        {/* Apply to Another */}
        <TouchableOpacity style={styles.applyAnother} onPress={applyToAnother}>
          <Text style={styles.applyAnotherText}>Apply to Another</Text>
          <Icon name="arrow-forward" size={20} color="#2196F3" />
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212121',
    marginTop: 12,
  },
  comparisonContainer: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 16,
  },
  imageComparison: {
    width: '100%',
    height: 250,
    borderRadius: 12,
    overflow: 'hidden',
    position: 'relative',
    marginBottom: 12,
  },
  comparisonImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  beforeImageContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: '100%',
    overflow: 'hidden',
  },
  dividerLine: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    width: 3,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  dividerHandle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#2196F3',
  },
  labelsContainer: {
    position: 'absolute',
    top: 12,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
  },
  beforeLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  afterLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  parametersContainer: {
    marginBottom: 30,
  },
  parametersBox: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  parameterText: {
    fontSize: 14,
    fontFamily: 'monospace',
    color: '#212121',
    marginBottom: 8,
  },
  actionsContainer: {
    marginBottom: 20,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
  },
  primaryButton: {
    backgroundColor: '#2196F3',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  secondaryButton: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#2196F3',
  },
  primaryButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginLeft: 8,
  },
  secondaryButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2196F3',
    marginLeft: 8,
  },
  applyAnother: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
  },
  applyAnotherText: {
    fontSize: 16,
    color: '#2196F3',
    marginRight: 8,
  },
});

export default ResultsScreen;
