import { useEffect, useState } from 'react';
import { CameraView } from 'capacitor-camera-view';
import './CameraScanner.css';

const CameraScanner = ({ onCapture, onOpenSettings, onOpenInfo }) => {
  const [isCameraActive, setIsCameraActive] = useState(false);

  useEffect(() => {
    startCamera();
    
    return () => {
      // Encountered a bug to where the screen goes blank whenever you touch a page without camera starting.
      // Removes the class when component unmounts
      document.body.classList.remove('camera-running');
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      // Request permissions
      const permissions = await CameraView.requestPermissions();
      
      if (permissions.camera !== 'granted') {
        alert('Camera permission is required');
        return;
      }

      console.log('Permissions granted, waiting before start...');
      
      // Delay to let iOS camera system initialize
      await new Promise(resolve => setTimeout(resolve, 500));

      console.log('Starting camera...');
      
      // Start the camera
      await CameraView.start({
        position: 'back'
      });

      // Adds CSS class to make WebView transparent
      document.body.classList.add('camera-running');
      
      setIsCameraActive(true);
      console.log('Camera started successfully!');
      
    } catch (error) {
      console.error('Camera start error:', error);
      alert(`Camera failed to start: ${error.message}`);
    }
  };

  const stopCamera = async () => {
    try {
      // Remove transparency class first
      document.body.classList.remove('camera-running');
      
      // Small delay before stopping
      await new Promise(resolve => setTimeout(resolve, 100));
      
      await CameraView.stop();
      setIsCameraActive(false);
      console.log('Camera stopped');
    } catch (error) {
      console.error('Error stopping camera:', error);
    }
  };

  const captureImage = async () => {
    if (!isCameraActive) {
      alert('Camera is not ready');
      return;
    }

    try {
      console.log('Capturing image...');
      
      // Capture with the new plugin
      const result = await CameraView.capture({
        quality: 90,
        saveToFile: false // Returns base64 string
      });
      
      console.log('Image captured successfully');
      
      if (onCapture) {
        onCapture({
          image: result.photo, // Base64 string
          settings: {
            aspectRatio: '16:9',
            chessboardCols: 9,
            chessboardRows: 6,
            squareSize: 30
          }
        });
      }
      
    } catch (error) {
      console.error('Capture error:', error);
      alert(`Capture failed: ${error.message}`);
    }
  };

  return (
    <div className="camera-container camera-modal">

      {/* Top control bar - TI Theme */}
      <div className="top-controls">
        <button 
          className="icon-btn info-btn"
          onClick={onOpenInfo}
        >
          ⓘ
        </button>

        <div className="app-title">KEYSTONE CORRECTION</div>

        <button 
          className="icon-btn settings-btn"
          onClick={onOpenSettings}
        >
          ⚙︎
        </button>
      </div>

      {/* Leveling icon */}
      <div className="guide-overlay">
        <div className="crosshair-container">
          <div className="tick up"></div>
          <div className="tick down"></div>
          <div className="tick left"></div>
          <div className="tick right"></div>
        </div>
      </div>

      {/* Capture button */}
      <div className="bottom-controls">
        <button 
          className="capture-button"
          onClick={captureImage}
          disabled={!isCameraActive}
        >
          <div className="capture-ring">
            <div className="capture-circle"></div>
          </div>
        </button>
      </div>
    </div>
  );
};

export default CameraScanner;