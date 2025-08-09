import React, { useState } from 'react';

const RescuePlanModal = ({ opportunity, isOpen, onClose, onSave }) => {
  const [selectedTasks, setSelectedTasks] = useState([]);
  const [notes, setNotes] = useState('');

  if (!isOpen || !opportunity) return null;

  const rescueTasks = [
    {
      id: 'immediate_contact',
      title: 'Immediate Contact',
      description: 'Reach out to the decision maker within 24 hours',
      priority: 'high',
      estimatedTime: '30 min',
      category: 'communication'
    },
    {
      id: 'value_prop_refresh',
      title: 'Refresh Value Proposition',
      description: 'Update and personalize the value proposition based on recent interactions',
      priority: 'high',
      estimatedTime: '2 hours',
      category: 'strategy'
    },
    {
      id: 'stakeholder_mapping',
      title: 'Stakeholder Mapping',
      description: 'Identify and engage additional stakeholders in the buying process',
      priority: 'medium',
      estimatedTime: '1 hour',
      category: 'research'
    },
    {
      id: 'competitive_analysis',
      title: 'Competitive Analysis',
      description: 'Analyze competitive landscape and position our solution',
      priority: 'medium',
      estimatedTime: '3 hours',
      category: 'research'
    },
    {
      id: 'demo_refresh',
      title: 'Refresh Demo',
      description: 'Update product demonstration with latest features and use cases',
      priority: 'medium',
      estimatedTime: '2 hours',
      category: 'presentation'
    },
    {
      id: 'case_study',
      title: 'Share Case Study',
      description: 'Provide relevant customer success stories and case studies',
      priority: 'low',
      estimatedTime: '1 hour',
      category: 'content'
    },
    {
      id: 'discount_strategy',
      title: 'Discount Strategy',
      description: 'Consider strategic pricing adjustments to accelerate deal',
      priority: 'low',
      estimatedTime: '30 min',
      category: 'pricing'
    }
  ];

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'communication':
        return '📞';
      case 'strategy':
        return '🎯';
      case 'research':
        return '🔍';
      case 'presentation':
        return '📊';
      case 'content':
        return '📄';
      case 'pricing':
        return '💰';
      default:
        return '📋';
    }
  };

  const handleTaskToggle = (taskId) => {
    setSelectedTasks(prev => 
      prev.includes(taskId) 
        ? prev.filter(id => id !== taskId)
        : [...prev, taskId]
    );
  };

  const handleSave = () => {
    const rescuePlan = {
      opportunityId: opportunity.Id,
      tasks: selectedTasks,
      notes,
      createdAt: new Date().toISOString(),
      estimatedCompletion: selectedTasks.length * 2 // Rough estimate in hours
    };
    onSave(rescuePlan);
    onClose();
  };

  const selectedTasksData = rescueTasks.filter(task => selectedTasks.includes(task.id));
  const totalEstimatedTime = selectedTasksData.reduce((sum, task) => sum + parseFloat(task.estimatedTime), 0);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Rescue Plan</h2>
              <p className="text-sm text-gray-500">
                Opportunity {opportunity.Id} • Health Score: {opportunity.health_score || 0}%
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          {/* Risk Analysis */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Risk Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <span className="text-red-500">🚨</span>
                  <span className="text-sm font-medium text-red-800">High Risk Factors</span>
                </div>
                <ul className="mt-2 text-sm text-red-700 space-y-1">
                  <li>• {opportunity.DaysInStage} days in current stage</li>
                  <li>• {opportunity.LastActivityDays} days since last activity</li>
                  {opportunity.SupportCases > 0 && (
                    <li>• {opportunity.SupportCases} support cases open</li>
                  )}
                </ul>
              </div>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <span className="text-yellow-500">⚠️</span>
                  <span className="text-sm font-medium text-yellow-800">Engagement Issues</span>
                </div>
                <ul className="mt-2 text-sm text-yellow-700 space-y-1">
                  <li>• Low email engagement ({opportunity.EmailOpens} opens)</li>
                  <li>• Limited meetings ({opportunity.MeetingsScheduled} scheduled)</li>
                  <li>• Reduced communication frequency</li>
                </ul>
              </div>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <span className="text-blue-500">💡</span>
                  <span className="text-sm font-medium text-blue-800">Opportunities</span>
                </div>
                <ul className="mt-2 text-sm text-blue-700 space-y-1">
                  <li>• High deal value: ${opportunity.Amount?.toLocaleString()}</li>
                  <li>• {opportunity.Industry} industry expertise</li>
                  <li>• {opportunity.Region} market knowledge</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Recommended Tasks */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-3">Recommended Rescue Tasks</h3>
            <div className="space-y-3">
              {rescueTasks.map((task) => (
                <div
                  key={task.id}
                  className={`border rounded-lg p-4 transition-all duration-200 ${
                    selectedTasks.includes(task.id)
                      ? 'border-athena-500 bg-athena-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <input
                      type="checkbox"
                      checked={selectedTasks.includes(task.id)}
                      onChange={() => handleTaskToggle(task.id)}
                      className="mt-1 h-4 w-4 text-athena-600 border-gray-300 rounded focus:ring-athena-500"
                    />
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-lg">{getCategoryIcon(task.category)}</span>
                        <h4 className="text-sm font-medium text-gray-900">{task.title}</h4>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </span>
                        <span className="text-xs text-gray-500">• {task.estimatedTime}</span>
                      </div>
                      <p className="text-sm text-gray-600">{task.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Notes */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-athena-500 focus:border-athena-500"
              placeholder="Add any additional context or specific actions..."
            />
          </div>

          {/* Summary */}
          {selectedTasks.length > 0 && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Rescue Plan Summary</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Selected Tasks:</span>
                  <span className="ml-2 font-medium text-gray-900">{selectedTasks.length}</span>
                </div>
                <div>
                  <span className="text-gray-500">Estimated Time:</span>
                  <span className="ml-2 font-medium text-gray-900">{totalEstimatedTime} hours</span>
                </div>
                <div>
                  <span className="text-gray-500">Priority:</span>
                  <span className="ml-2 font-medium text-gray-900">
                    {selectedTasksData.some(t => t.priority === 'high') ? 'High' : 'Medium'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div className="flex justify-end space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors duration-200"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={selectedTasks.length === 0}
              className="px-4 py-2 text-sm font-medium text-white bg-athena-600 border border-transparent rounded-md hover:bg-athena-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              Save Rescue Plan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RescuePlanModal;
