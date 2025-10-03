import { TrendingUp, Users, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface MetricsCardProps {
  metrics: any;
}

export default function MetricsCard({ metrics }: MetricsCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-slate-900">Screening Metrics</h2>
        <TrendingUp className="w-6 h-6 text-blue-600" />
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Users className="w-5 h-5 text-slate-600" />
            <span className="text-sm font-medium text-slate-600">Total</span>
          </div>
          <div className="text-2xl font-bold text-slate-900">{metrics.total_screened || 0}</div>
        </div>

        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className="text-sm font-medium text-green-600">Approved</span>
          </div>
          <div className="text-2xl font-bold text-green-900">{metrics.approved || 0}</div>
          <div className="text-xs text-green-600 mt-1">{metrics.percentages?.approved || 0}%</div>
        </div>

        <div className="bg-yellow-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <span className="text-sm font-medium text-yellow-600">Review</span>
          </div>
          <div className="text-2xl font-bold text-yellow-900">{metrics.review || 0}</div>
          <div className="text-xs text-yellow-600 mt-1">{metrics.percentages?.review || 0}%</div>
        </div>

        <div className="bg-red-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <XCircle className="w-5 h-5 text-red-600" />
            <span className="text-sm font-medium text-red-600">Blocked</span>
          </div>
          <div className="text-2xl font-bold text-red-900">{metrics.blocked || 0}</div>
          <div className="text-xs text-red-600 mt-1">{metrics.percentages?.blocked || 0}%</div>
        </div>
      </div>

      {/* Rule Breakdown */}
      <div>
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Decisions by Rule</h3>
        <div className="space-y-2">
          {Object.entries(metrics.by_rule || {}).map(([ruleId, count]: [string, any]) => (
            <div key={ruleId} className="flex items-center justify-between p-2 bg-slate-50 rounded">
              <span className="text-sm text-slate-700">{ruleId}</span>
              <span className="text-sm font-medium text-slate-900">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {metrics.last_updated && (
        <div className="mt-4 pt-4 border-t border-slate-200">
          <p className="text-xs text-slate-500">
            Last updated: {new Date(metrics.last_updated).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}
