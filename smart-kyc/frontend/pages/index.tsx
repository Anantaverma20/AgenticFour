// index.tsx
// Upload & screening UI (placeholder)

import { useState } from 'react';
import Head from 'next/head';
import UploadCard from '../components/UploadCard';
import AnalystPanel from '../components/AnalystPanel';
import MetricsCard from '../components/MetricsCard';
import ResultsTable from '../components/ResultsTable';
import TeachRuleModal from '../components/TeachRuleModal';
import { Upload, Shield, BarChart3 } from 'lucide-react';

export default function Home() {
  const [results, setResults] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const [selectedCase, setSelectedCase] = useState<any>(null);
  const [showTeachModal, setShowTeachModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'upload' | 'results' | 'metrics'>('upload');

  const handleUploadComplete = (data: any) => {
    setResults(data.results || []);
    setMetrics(data.metrics);
    setActiveTab('results');
  };

  const handleCaseSelect = (caseData: any) => {
    setSelectedCase(caseData);
  };

  const handleTeachRule = () => {
    setShowTeachModal(true);
  };

  return (
    <>
      <Head>
        <title>Smart KYC Screener</title>
        <meta name="description" content="AI-powered KYC screening with human-in-the-loop" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Shield className="w-8 h-8 text-blue-600" />
                <div>
                  <h1 className="text-2xl font-bold text-slate-900">Smart KYC Screener</h1>
                  <p className="text-sm text-slate-600">AI-Powered Compliance Automation</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition ${activeTab === 'upload' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}
                >
                  <Upload className="w-4 h-4" />
                  <span>Upload</span>
                </button>
                <button
                  onClick={() => setActiveTab('metrics')}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition ${activeTab === 'metrics' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>Metrics</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Upload & Results */}
            <div className="lg:col-span-2 space-y-6">
              {activeTab === 'upload' && (
                <UploadCard onUploadComplete={handleUploadComplete} />
              )}

              {activeTab === 'results' && results.length > 0 && (
                <ResultsTable
                  results={results}
                  onCaseSelect={handleCaseSelect}
                />
              )}

              {activeTab === 'metrics' && metrics && (
                <MetricsCard metrics={metrics} />
              )}
            </div>

            {/* Right Column - Analyst Panel */}
            <div className="lg:col-span-1">
              <AnalystPanel
                selectedCase={selectedCase}
                onTeachRule={handleTeachRule}
              />
            </div>
          </div>
        </main>

        {/* Teach Rule Modal */}
        {showTeachModal && (
          <TeachRuleModal
            onClose={() => setShowTeachModal(false)}
            onRuleAdded={() => {
              setShowTeachModal(false);
            }}
          />
        )}
      </div>
    </>
  );
}
