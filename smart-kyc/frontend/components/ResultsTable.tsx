import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface ResultsTableProps {
  results: any[];
  onCaseSelect: (caseData: any) => void;
}

export default function ResultsTable({ results, onCaseSelect }: ResultsTableProps) {
  const getDecisionBadge = (decision: string) => {
    switch (decision) {
      case 'APPROVE':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
            <CheckCircle className="w-4 h-4 mr-1" />
            Approved
          </span>
        );
      case 'REVIEW':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
            <AlertTriangle className="w-4 h-4 mr-1" />
            Review
          </span>
        );
      case 'BLOCK':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
            <XCircle className="w-4 h-4 mr-1" />
            Blocked
          </span>
        );
      default:
        return <span className="text-slate-500">Unknown</span>;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-200">
        <h2 className="text-xl font-bold text-slate-900">Screening Results</h2>
        <p className="text-sm text-slate-600 mt-1">{results.length} applicant(s) processed</p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Country</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Decision</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Match Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Adverse Media</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Action</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {results.map((result, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-slate-900">{result.applicant?.name}</div>
                  <div className="text-sm text-slate-500">{result.applicant?.email}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                  {result.applicant?.country}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getDecisionBadge(result.decision)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                  {result.match_result?.match_score || 0}%
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                  {result.adverse_media_count || 0} article(s)
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button
                    onClick={() => onCaseSelect(result)}
                    className="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
