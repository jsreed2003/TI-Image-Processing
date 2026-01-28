/**
 * Home Screen
 * Main landing screen with options to start camera or choose image
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

const HomeScreen = ({navigation}) => {
  const recentCorrections = [
    {id: 1, location: 'Living Room', time: '2 hours ago'},
    {id: 2, location: 'Bedroom', time: 'Yesterday'},
    {id: 3, location: 'Office', time: '3 days ago'},
  ];

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#2196F3" />
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* App Branding */}
        <View style={styles.header}>
          <Icon name="videocam" size={80} color="#2196F3" />
          <Text style={styles.title}>Keystone Correction</Text>
          <Text style={styles.subtitle}>
            Simple. Automatic. Correction.
          </Text>
        </View>

        {/* Main Actions */}
        <View style={styles.actionsContainer}>
          <TouchableOpacity
            style={[styles.button, styles.primaryButton]}
            onPress={() => navigation.navigate('Camera')}>
            <Icon name="camera-alt" size={24} color="#fff" />
            <Text style={styles.primaryButtonText}>Start Camera</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.secondaryButton]}
            onPress={() => {
              /* TODO: Implement image picker */
              alert('Image picker coming soon!');
            }}>
            <Icon name="folder" size={24} color="#2196F3" />
            <Text style={styles.secondaryButtonText}>Choose Image</Text>
          </TouchableOpacity>
        </View>

        {/* Recent Corrections */}
        <View style={styles.recentContainer}>
          <Text style={styles.recentTitle}>Recent Corrections</Text>
          {recentCorrections.map(item => (
            <TouchableOpacity
              key={item.id}
              style={styles.recentItem}
              onPress={() => {
                /* TODO: Load saved correction */
              }}>
              <Icon name="history" size={20} color="#757575" />
              <View style={styles.recentTextContainer}>
                <Text style={styles.recentLocation}>{item.location}</Text>
                <Text style={styles.recentTime}>{item.time}</Text>
              </View>
              <Icon name="chevron-right" size={20} color="#BDBDBD" />
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Settings Button (Top Right) */}
      <TouchableOpacity
        style={styles.settingsButton}
        onPress={() => navigation.navigate('Settings')}>
        <Icon name="settings" size={24} color="#757575" />
      </TouchableOpacity>

      {/* Help Button (Top Right) */}
      <TouchableOpacity
        style={styles.helpButton}
        onPress={() => navigation.navigate('Help')}>
        <Icon name="help-outline" size={24} color="#757575" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  scrollContent: {
    padding: 20,
    paddingTop: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212121',
    marginTop: 16,
  },
  subtitle: {
    fontSize: 16,
    color: '#757575',
    marginTop: 8,
  },
  actionsContainer: {
    marginBottom: 40,
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
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#2196F3',
  },
  primaryButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginLeft: 8,
  },
  secondaryButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2196F3',
    marginLeft: 8,
  },
  recentContainer: {
    marginTop: 20,
  },
  recentTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212121',
    marginBottom: 12,
  },
  recentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    marginBottom: 8,
  },
  recentTextContainer: {
    flex: 1,
    marginLeft: 12,
  },
  recentLocation: {
    fontSize: 16,
    color: '#212121',
  },
  recentTime: {
    fontSize: 14,
    color: '#757575',
    marginTop: 2,
  },
  settingsButton: {
    position: 'absolute',
    top: 10,
    right: 60,
    padding: 10,
  },
  helpButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    padding: 10,
  },
});

export default HomeScreen;
