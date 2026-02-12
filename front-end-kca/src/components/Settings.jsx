import { useState, useEffect } from 'react';
import './Settings.css';

const Settings = ({ onBack, settings, onSave }) => {
  const [localSettings, setLocalSettings] = useState(settings || {
    aspectRatio: '16:9',
    chessboardCols: 9,
    chessboardRows: 6,
    squareSize: 30
  });

  const handleSave = () => {
    if (onSave) {
      onSave(localSettings);
    }
    onBack();
  };

  return (
    <div className="settings-page">
      <div className="settings-page-header">
        <button className="back-btn" onClick={onBack}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <h2>Settings</h2>
        <div style={{width: '70px'}}></div>
      </div>

      <div className="settings-page-content">
        <div className="setting-group">
          <label>Aspect Ratio</label>
          <select 
            value={localSettings.aspectRatio}
            onChange={(e) => setLocalSettings({...localSettings, aspectRatio: e.target.value})}
          >
            <option value="16:9">16:9 (Standard)</option>
            <option value="16:10">16:10 (WXGA)</option>
            <option value="4:3">4:3 (Traditional)</option>
            <option value="21:9">21:9 (Ultrawide)</option>
          </select>
        </div>

        <div className="setting-group">
          <label>Chessboard Columns</label>
          <input 
            type="number" 
            min="3" 
            max="20"
            value={localSettings.chessboardCols}
            onChange={(e) => setLocalSettings({...localSettings, chessboardCols: parseInt(e.target.value)})}
          />
        </div>

        <div className="setting-group">
          <label>Chessboard Rows</label>
          <input 
            type="number" 
            min="3" 
            max="20"
            value={localSettings.chessboardRows}
            onChange={(e) => setLocalSettings({...localSettings, chessboardRows: parseInt(e.target.value)})}
          />
        </div>

        <div className="setting-group">
          <label>Square Size (mm)</label>
          <input 
            type="number" 
            min="10" 
            max="100"
            step="5"
            value={localSettings.squareSize}
            onChange={(e) => setLocalSettings({...localSettings, squareSize: parseInt(e.target.value)})}
          />
        </div>

        <button className="btn-save-full" onClick={handleSave}>
          Save Settings
        </button>
      </div>
    </div>
  );
};

export default Settings;