import { useState } from 'react';
import axios from 'axios';
import { MessageSquare, FileText, AlertCircle, Sparkles } from 'lucide-react';

interface AnalystPanelProps {
  selectedCase: any;
  onTeachRule: () => void;
}

export default function AnalystPanel({ selectedCase, onTeachRule }: AnalystPanelProps) {
  const [activeTab, setActiveTab] = useState<'explanation' | 'adverse' | 'reports'>('explanation');
  const [adverseMedia, setAdverseMedia] = useState<any>(null);
  const [eddReport, setEddReport] = useState<string>('');
  const [sarReport, setSarReport] = useState<string>('');

  const loadAdverseMedia = async () => {
    if (!selectedCase?.applicant?.name) return;
    try {
      const response = await axios.get(`http://localhost:8000/adverse-media/${selectedCase.applicant.name}`);
      setAdverseMedia(response.data);
    } catch (error) {
      console.error('Error loading adverse media:', error);
    }
  };

  const loadEDD = async () => {
    if (!selectedCase) return;
    try {
      const response = await axios.post('http://localhost:8000/draft-edd', selectedCase);
      setEddReport(response.data.report);
    } catch (error) {
      console.error('Error loading EDD:', error);
    }
  };

  const loadSAR = async () => {
    if (!selectedCase) return;
    try {
      const response = await axios.post('http://localhost:8000/draft-sar', selectedCase);
      setSarReport(response.data.report);
    } catch (error) {
      console.error('Error loading SAR:', error);
    }
  };

  if (!selectedCase) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="text-center py-12">
          <MessageSquare className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-500">Select a case to view details</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 text-white">
        <div className="flex items-center space-x-2 mb-2">
          <Sparkles className="w-5 h-5" />
          <h3 className="font-semibold">AI Copilot</h3>
        </div>
        <p className="text-sm opacity-90">{selectedCase.applicant.name}</p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200">
        <button
          onClick={() => setActiveTab('explanation')}
          className={`flex-1 px-4 py-3 text-sm font-medium transition ${activeTab === 'explanation' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-600'}`}
        >
          Explanation
        </button>
        <button
          onClick={() => { setActiveTab('adverse'); loadAdverseMedia(); }}
          className={`flex-1 px-4 py-3 text-sm font-medium transition ${activeTab === 'adverse' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-600'}`}
        >
          Adverse Media
        </button>
        <button
          onClick={() => { setActiveTab('reports'); loadEDD(); loadSAR(); }}
          className={`flex-1 px-4 py-3 text-sm font-medium transition ${activeTab === 'reports' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-slate-600'}`}
        >
          Reports
        </button>
      </div>

      {/* Content */}
      <div className="p-6 max-h-[600px] overflow-y-auto">
        {activeTab === 'explanation' && (
          <div className="space-y-4">
            <div className="prose prose-sm max-w-none">
              <div dangerouslySetInnerHTML={{ __html: selectedCase.explanation?.explanation?.replace(/\n/g, '<br/>') || 'No explanation available' }} />
            </div>

            {selectedCase.explanation?.citations && selectedCase.explanation.citations.length > 0 && (
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <h4 className="text-sm font-semibold text-blue-900 mb-2">Citations</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  {selectedCase.explanation.citations.map((citation: any, idx: number) => (
                    <li key={idx}>• {citation.type}: {citation.description || citation.entity || citation.count}</li>
                  ))}
                </ul>
              </div>
            )}

            <button
              onClick={onTeachRule}
              className="w-full mt-4 px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg hover:from-purple-700 hover:to-purple-800 transition flex items-center justify-center space-x-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>Teach New Rule</span>
            </button>
          </div>
        )}

        {activeTab === 'adverse' && (
          <div className="space-y-4">
            {adverseMedia ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-slate-900">
                    {adverseMedia.total_hits} Article(s) Found
                  </h4>
                  {adverseMedia.max_severity && (
                    <span className={`px-2 py-1 rounded text-xs font-medium ${adverseMedia.max_severity === 'critical' ? 'bg-red-100 text-red-800' : adverseMedia.max_severity === 'high' ? 'bg-orange-100 text-orange-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {adverseMedia.max_severity.toUpperCase()}
                    </span>
                  )}
                </div>

                {adverseMedia.articles?.map((article: any, idx: number) => (
                  <div key={idx} className="p-4 border border-slate-200 rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="font-medium text-slate-900">{article.topic}</h5>
                      <span className="text-xs text-slate-500">{article.date}</span>
                    </div>
                    <p className="text-sm text-slate-600 mb-2">{article.snippet}</p>
                    <div className="flex flex-wrap gap-2">
                      {article.trigger_lines?.map((trigger: string, tidx: number) => (
                        <span key={tidx} className="px-2 py-1 bg-red-50 text-red-700 text-xs rounded">
                          {trigger}
                        </span>
                      ))}
                    </div>
                    <p className="text-xs text-slate-500 mt-2">Source: {article.source}</p>
                  </div>
                ))}
              </>
            ) : (
              <p className="text-slate-500 text-center py-8">Loading adverse media...</p>
            )}
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-slate-900 mb-2 flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>Enhanced Due Diligence (EDD)</span>
              </h4>
              <div className="p-4 bg-slate-50 rounded-lg text-xs font-mono whitespace-pre-wrap max-h-64 overflow-y-auto">
                {eddReport || 'Loading...'}
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-slate-900 mb-2 flex items-center space-x-2">
                <AlertCircle className="w-4 h-4" />
                <span>Suspicious Activity Report (SAR)</span>
              </h4>
              <div className="p-4 bg-slate-50 rounded-lg text-xs font-mono whitespace-pre-wrap max-h-64 overflow-y-auto">
                {sarReport || 'Loading...'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
