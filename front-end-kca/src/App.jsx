import { useState } from 'react';
import CameraScanner from './components/CameraScanner';
import Settings from './components/Settings';
import Info from './components/Info';
import { detectCorners } from './api';
import './App.css';

const DEFAULT_SETTINGS = {
  aspectRatio: '16:9',
  chessboardCols: 7,
  chessboardRows: 7,
  squareSize: 30,
};

function App() {
  const [capturedData, setCapturedData] = useState(null);
  const [currentView, setCurrentView] = useState('camera'); // 'camera', 'settings', 'info', 'results'
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [corners, setCorners] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCapture = async (data) => {
    setCapturedData(data);
    setCorners(null);
    setError(null);
    setCurrentView('results');
    setLoading(true);

    try {
      const result = await detectCorners(data.image, data.settings);
      setCorners(result);
    } catch (err) {
      console.error('Corner detection error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = (newSettings) => {
    setSettings(newSettings);
  };

  const handleOpenSettings = () => setCurrentView('settings');
  const handleOpenInfo = () => setCurrentView('info');

  const handleBackToCamera = () => {
    setCurrentView('camera');
    setCapturedData(null);
    setCorners(null);
    setError(null);
  };

  // Camera View
  if (currentView === 'camera') {
    return (
      <div className="App">
        <CameraScanner
          onCapture={handleCapture}
          onOpenSettings={handleOpenSettings}
          onOpenInfo={handleOpenInfo}
          settings={settings}
        />
      </div>
    );
  }

  // Settings Page
  if (currentView === 'settings') {
    return <Settings onBack={handleBackToCamera} settings={settings} onSave={handleSaveSettings} />;
  }

  // Info Page
  if (currentView === 'info') {
    return <Info onBack={handleBackToCamera} />;
  }

  // Results Page
  if (currentView === 'results' && capturedData) {
    const LABELS = ['Top-left', 'Top-right', 'Bottom-right', 'Bottom-left'];

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
            <h3>📐 Detected Corners</h3>
            {loading && <p className="placeholder-text">Analyzing image...</p>}
            {error && (
              <p className="placeholder-text" style={{color: '#e05a5a', whiteSpace: 'pre-line'}}>
                {error}
              </p>
            )}
            {corners && (
              <div className="settings-info">
                {LABELS.map((label, i) => (
                  <div className="info-row" key={label}>
                    <span className="label">{label}:</span>
                    <span className="value">
                      ({corners.originalCorners[i][0].toFixed(0)}, {corners.originalCorners[i][1].toFixed(0)})
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {corners && (
            <div className="results-section">
              <h3>Optimal Rectangle</h3>
              <div className="settings-info">
                {LABELS.map((label, i) => (
                  <div className="info-row" key={label}>
                    <span className="label">{label}:</span>
                    <span className="value">
                      ({corners.optimalCorners[i][0].toFixed(0)}, {corners.optimalCorners[i][1].toFixed(0)})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {corners && corners.optimalInputCorners && (
            <div className="results-section">
              <h3>Optimal Input Corners</h3>
              <div className="settings-info">
                {LABELS.map((label, i) => (
                  <div className="info-row" key={label}>
                    <span className="label">{label}:</span>
                    <span className="value">
                      ({corners.optimalInputCorners[i][0].toFixed(0)}, {corners.optimalInputCorners[i][1].toFixed(0)})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return null;
}

export default App;
