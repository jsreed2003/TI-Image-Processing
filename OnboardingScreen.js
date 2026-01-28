/**
 * Onboarding Screen - Simple placeholder
 * TODO: Implement full 3-screen onboarding flow
 */

import React from 'react';
import {View, Text, TouchableOpacity, StyleSheet} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

export const OnboardingScreen = ({navigation}) => {
  return (
    <View style={styles.container}>
      <Icon name="videocam" size={100} color="#2196F3" />
      <Text style={styles.title}>Welcome to{'\n'}Keystone Correction</Text>
      <Text style={styles.subtitle}>
        Automatically fix distorted projections with just your phone camera
      </Text>
      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.replace('Home')}>
        <Text style={styles.buttonText}>Get Started</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.replace('Home')}>
        <Text style={styles.skipText}>Skip</Text>
      </TouchableOpacity>
    </View>
  );
};

/**
 * Settings Screen - Simple placeholder
 * TODO: Implement full settings functionality
 */

export const SettingsScreen = () => {
  return (
    <View style={styles.container}>
      <Icon name="settings" size={80} color="#2196F3" />
      <Text style={styles.title}>Settings</Text>
      <Text style={styles.subtitle}>Settings screen coming soon!</Text>
    </View>
  );
};

/**
 * Help Screen - Simple placeholder
 * TODO: Implement full help/FAQ content
 */

export const HelpScreen = () => {
  return (
    <View style={styles.container}>
      <Icon name="help-outline" size={80} color="#2196F3" />
      <Text style={styles.title}>Help & FAQ</Text>
      <Text style={styles.subtitle}>Help content coming soon!</Text>
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
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212121',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: '#757575',
    textAlign: 'center',
    marginBottom: 40,
  },
  button: {
    backgroundColor: '#2196F3',
    paddingHorizontal: 40,
    paddingVertical: 16,
    borderRadius: 8,
    marginBottom: 20,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  skipText: {
    fontSize: 16,
    color: '#757575',
  },
});
