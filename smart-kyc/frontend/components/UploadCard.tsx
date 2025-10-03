import { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, Image, Loader2 } from 'lucide-react';

interface UploadCardProps {
  onUploadComplete: (data: any) => void;
}

export default function UploadCard({ onUploadComplete }: UploadCardProps) {
  const [uploadType, setUploadType] = useState<'csv' | 'id'>('csv');
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileUpload = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = uploadType === 'csv' ? '/upload-csv' : '/upload-id';
      const response = await axios.post(`http://localhost:8000${endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onUploadComplete(response.data);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFileUpload(file);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-slate-900 mb-4">Upload for Screening</h2>
      
      {/* Upload Type Toggle */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setUploadType('csv')}
          className={`flex-1 py-2 px-4 rounded-lg flex items-center justify-center space-x-2 transition ${uploadType === 'csv' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'}`}
        >
          <FileText className="w-4 h-4" />
          <span>CSV Batch</span>
        </button>
        <button
          onClick={() => setUploadType('id')}
          className={`flex-1 py-2 px-4 rounded-lg flex items-center justify-center space-x-2 transition ${uploadType === 'id' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'}`}
        >
          <Image className="w-4 h-4" />
          <span>ID Document</span>
        </button>
      </div>

      {/* Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300 bg-slate-50'}`}
      >
        {uploading ? (
          <div className="flex flex-col items-center space-y-3">
            <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
            <p className="text-slate-600">Processing...</p>
          </div>
        ) : (
          <div>
            <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-slate-700 mb-2">
              {uploadType === 'csv' ? 'Upload CSV File' : 'Upload ID Document'}
            </p>
            <p className="text-sm text-slate-500 mb-4">
              Drag and drop or click to browse
            </p>
            <label className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition">
              Choose File
              <input
                type="file"
                accept={uploadType === 'csv' ? '.csv' : 'image/*'}
                onChange={handleFileInput}
                className="hidden"
              />
            </label>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="mt-4 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-900">
          {uploadType === 'csv' 
            ? 'Upload a CSV with columns: name, email, country, dob, document_type'
            : 'Upload a passport or driver\'s license for DPT-2 extraction'}
        </p>
      </div>
    </div>
  );
}
