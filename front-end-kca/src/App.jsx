import { useState } from 'react';
import CameraScanner from './components/CameraScanner';
import Settings from './components/Settings';
import Info from './components/Info';
import './App.css';

function App() {
  const [capturedData, setCapturedData] = useState(null);
  const [currentView, setCurrentView] = useState('camera'); // 'camera', 'settings', 'info', 'results'

  const handleCapture = (data) => {
    console.log('Captured data:', {
      imageLength: data.image.length,
      settings: data.settings
    });
    
    setCapturedData(data);
    setCurrentView('results');
  };

  const handleOpenSettings = () => {
    setCurrentView('settings');
  };

  const handleOpenInfo = () => {
    setCurrentView('info');
  };

  const handleBackToCamera = () => {
    setCurrentView('camera');
    setCapturedData(null);
  };

  // Camera View
  if (currentView === 'camera') {
    return (
      <div className="App">
        <CameraScanner 
          onCapture={handleCapture}
          onOpenSettings={handleOpenSettings}
          onOpenInfo={handleOpenInfo}
        />
      </div>
    );
  }

  // Settings Page
  if (currentView === 'settings') {
    return <Settings onBack={handleBackToCamera} />;
  }

  // Info Page
  if (currentView === 'info') {
    return <Info onBack={handleBackToCamera} />;
  }

  // Results Page
  if (currentView === 'results' && capturedData) {
    return (
      <div className="results-screen">
        <div className="results-header">
          <button className="back-btn" onClick={handleBackToCamera}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back
          </button>
          <h2>Correction Results</h2>
          <div style={{width: '70px'}}></div>
        </div>

        <div className="results-content">
          <div className="results-section">
            <h3>📸 Captured Image</h3>
            <div className="image-preview">
              <img src={`data:image/jpeg;base64,${capturedData.image}`} alt="Captured" />
            </div>
          </div>

          <div className="results-section">
            <h3>⚙️ Settings Used</h3>
            <div className="settings-info">
              <div className="info-row">
                <span className="label">Aspect Ratio:</span>
                <span className="value">{capturedData.settings.aspectRatio}</span>
              </div>
              <div className="info-row">
                <span className="label">Chessboard:</span>
                <span className="value">{capturedData.settings.chessboardCols} × {capturedData.settings.chessboardRows}</span>
              </div>
              <div className="info-row">
                <span className="label">Square Size:</span>
                <span className="value">{capturedData.settings.squareSize}mm</span>
              </div>
            </div>
          </div>

          <div className="results-section">
            <h3>📐 Next Steps</h3>
            <p className="placeholder-text">
              Corner coordinates will be calculated here once Jackson completes backend and integration is done.
              <br/><br/>
              Expected output: Top-left, Top-right, Bottom-left, Bottom-right corner positions.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

export default App;