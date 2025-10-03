import { useState } from 'react';
import axios from 'axios';
import { X, Plus, Trash2 } from 'lucide-react';

interface TeachRuleModalProps {
  onClose: () => void;
  onRuleAdded: () => void;
}

export default function TeachRuleModal({ onClose, onRuleAdded }: TeachRuleModalProps) {
  const [ruleId, setRuleId] = useState('');
  const [description, setDescription] = useState('');
  const [outcome, setOutcome] = useState<'APPROVE' | 'REVIEW' | 'BLOCK'>('REVIEW');
  const [priority, setPriority] = useState(50);
  const [conditions, setConditions] = useState<any[]>([
    { field: '', op: 'equals', value: '' }
  ]);
  const [submitting, setSubmitting] = useState(false);

  const addCondition = () => {
    setConditions([...conditions, { field: '', op: 'equals', value: '' }]);
  };

  const removeCondition = (index: number) => {
    setConditions(conditions.filter((_, i) => i !== index));
  };

  const updateCondition = (index: number, key: string, value: any) => {
    const updated = [...conditions];
    updated[index] = { ...updated[index], [key]: value };
    setConditions(updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await axios.post('http://localhost:8000/teach-rule', {
        rule_id: ruleId,
        description,
        outcome,
        priority,
        conditions,
        enabled: true
      });
      alert('Rule added successfully!');
      onRuleAdded();
    } catch (error) {
      console.error('Error adding rule:', error);
      alert('Failed to add rule');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">Teach New Rule</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Rule ID */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Rule ID
            </label>
            <input
              type="text"
              value={ruleId}
              onChange={(e) => setRuleId(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., high_value_transaction"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe what this rule does..."
              rows={3}
              required
            />
          </div>

          {/* Outcome */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Outcome
            </label>
            <select
              value={outcome}
              onChange={(e) => setOutcome(e.target.value as any)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="APPROVE">Approve</option>
              <option value="REVIEW">Review</option>
              <option value="BLOCK">Block</option>
            </select>
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Priority (lower = higher priority)
            </label>
            <input
              type="number"
              value={priority}
              onChange={(e) => setPriority(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              min="1"
              max="999"
            />
          </div>

          {/* Conditions */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-slate-700">
                Conditions
              </label>
              <button
                type="button"
                onClick={addCondition}
                className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
              >
                <Plus className="w-4 h-4" />
                <span>Add Condition</span>
              </button>
            </div>

            <div className="space-y-3">
              {conditions.map((condition, index) => (
                <div key={index} className="flex items-center space-x-2 p-3 bg-slate-50 rounded-lg">
                  <input
                    type="text"
                    value={condition.field}
                    onChange={(e) => updateCondition(index, 'field', e.target.value)}
                    className="flex-1 px-3 py-2 border border-slate-300 rounded text-sm"
                    placeholder="Field (e.g., country)"
                  />
                  <select
                    value={condition.op}
                    onChange={(e) => updateCondition(index, 'op', e.target.value)}
                    className="px-3 py-2 border border-slate-300 rounded text-sm"
                  >
                    <option value="equals">equals</option>
                    <option value="gte">≥</option>
                    <option value="gt">&gt;</option>
                    <option value="lte">≤</option>
                    <option value="lt">&lt;</option>
                    <option value="in">in</option>
                    <option value="contains">contains</option>
                  </select>
                  <input
                    type="text"
                    value={condition.value}
                    onChange={(e) => updateCondition(index, 'value', e.target.value)}
                    className="flex-1 px-3 py-2 border border-slate-300 rounded text-sm"
                    placeholder="Value"
                  />
                  {conditions.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeCondition(index)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-6 py-2 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg hover:from-purple-700 hover:to-purple-800 transition disabled:opacity-50"
            >
              {submitting ? 'Adding...' : 'Add Rule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
