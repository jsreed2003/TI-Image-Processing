// === React PWA Frontend (Vite + Axios + Chart.js) ===
// Run: npm install && npm run dev
// This is App.jsx

import { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

export default function App() {
  const [original, setOriginal] = useState(null);
  const [reference, setReference] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [quality, setQuality] = useState(75);
  const [compressionData, setCompressionData] = useState([]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('distorted', original);
    if (reference) formData.append('reference', reference);

    const res = await axios.post('http://localhost:8000/iq-metrics/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    setMetrics(res.data);
  };

  const handleCompress = async () => {
    const formData = new FormData();
    formData.append('image', original);
    formData.append('quality', quality);

    const res = await axios.post('http://localhost:8000/compress/', formData);
    setCompressionData(prev => [...prev, { quality, size: res.data.compressed_size }]);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-xl font-bold mb-2">Image Quality Analyzer</h1>

      <label className="block mb-2">Upload Image (Required)</label>
      <input type="file" onChange={e => setOriginal(e.target.files[0])} className="mb-4" />

      <label className="block mb-2">Reference Image (Optional)</label>
      <input type="file" onChange={e => setReference(e.target.files[0])} className="mb-4" />

      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">Analyze</button>

      {metrics && (
        <div className="mt-4">
          <pre>{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      )}

      <div className="mt-8">
        <label className="block mb-2">JPEG Quality: {quality}</label>
        <input type="range" min="10" max="100" value={quality} onChange={e => setQuality(+e.target.value)} />
        <button onClick={handleCompress} className="ml-4 bg-green-600 text-white px-4 py-2 rounded">Compress</button>
      </div>

      {compressionData.length > 0 && (
        <div className="mt-6">
          <Line data={{
            labels: compressionData.map(p => p.quality),
            datasets: [
              {
                label: 'Compressed Size (bytes)',
                data: compressionData.map(p => p.size),
                borderColor: 'rgba(75,192,192,1)',
                tension: 0.3
              }
            ]
          }} />
        </div>
      )}
    </div>
  );
}
