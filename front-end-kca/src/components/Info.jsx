import './Info.css';

const Info = ({ onBack }) => {
  return (
    <div className="info-page">
      <div className="info-page-header">
        <button className="back-btn" onClick={onBack}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <h2>How to Use</h2>
        <div style={{width: '70px'}}></div>
      </div>
      

      <div className="info-page-content">
        {/* CRITICAL POSITIONING INFO - Emphasized */}
        <div className="critical-info-box">
          <div className="critical-icon">⚠️</div>
          <div className="critical-content">
            <h3>IMPORTANT: Camera Position</h3>
            <p>
              <strong>Position your phone camera where the audience will be sitting.</strong> 
              The keystone correction will be optimized for the camera's perspective. 
              For best results, stand at the center of where viewers will be located.
            </p>
          </div>
        </div>

        <div className="info-section">
          <div className="step-number">1</div>
          <div className="step-content">
            <h3>Setup Your Projector</h3>
            <p>Project a chessboard pattern onto a flat surface. Make sure the entire pattern is visible and well-lit.</p>
          </div>
        </div>

        <div className="info-section">
          <div className="step-number">2</div>
          <div className="step-content">
            <h3>Align the Camera</h3>
            <p>Point your phone camera at the projected chessboard. Try to capture the entire pattern within the frame.</p>
          </div>
        </div>

        <div className="info-section">
          <div className="step-number">3</div>
          <div className="step-content">
            <h3>Capture the Image</h3>
            <p>Tap the capture button when the pattern is clearly visible and steady.</p>
          </div>
        </div>

        <div className="info-section">
          <div className="step-number">4</div>
          <div className="step-content">
            <h3>Review Correction</h3>
            <p>The app will calculate corner coordinates and display the corrected projection outline.</p>
          </div>
        </div>

        <div className="info-tips">
          <h3>💡 Tips for Best Results</h3>
          <ul>
            <li>Use a white or light-colored projection surface</li>
            <li>Ensure good lighting conditions</li>
            <li>Keep your phone steady when capturing</li>
            <li>Configure chessboard settings to match your pattern</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Info;