import React from 'react';

const OpportunityCard = ({ opportunity, onViewDetails, onRescuePlan }) => {
  const {
    Id,
    Amount,
    StageName,
    Industry,
    Region,
    health_score,
    risk_level,
    DaysInStage,
    EmailOpens,
    EmailClicks,
    ContentDownloads,
    MeetingsScheduled,
    CallsMade,
    SupportCases,
    CriticalCases,
    LastActivityDays
  } = opportunity;

  const getHealthScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    if (score >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getRiskLevelColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'low':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskLevelIcon = (level) => {
    switch (level?.toLowerCase()) {
      case 'low':
        return '✅';
      case 'medium':
        return '⚠️';
      case 'high':
        return '🚨';
      case 'critical':
        return '🔥';
      default:
        return '❓';
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };



  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Opportunity {Id}</h3>
            <p className="text-sm text-gray-500">{Industry} • {Region}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(risk_level)}`}>
              {getRiskLevelIcon(risk_level)} {risk_level || 'Unknown'}
            </span>
          </div>
        </div>
      </div>

      {/* Health Score */}
      <div className="px-6 py-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-medium text-gray-700">Health Score</span>
          <span className={`px-3 py-1 rounded-full text-sm font-bold ${getHealthScoreColor(health_score)}`}>
            {health_score || 0}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              health_score >= 80 ? 'bg-green-500' :
              health_score >= 60 ? 'bg-yellow-500' :
              health_score >= 40 ? 'bg-orange-500' : 'bg-red-500'
            }`}
            style={{ width: `${health_score || 0}%` }}
          ></div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="px-6 py-4 border-t border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Deal Value</p>
            <p className="text-lg font-semibold text-gray-900">{formatCurrency(Amount)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Stage</p>
            <p className="text-lg font-semibold text-gray-900">{StageName}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Days in Stage</p>
            <p className="text-lg font-semibold text-gray-900">{DaysInStage}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Last Activity</p>
            <p className="text-lg font-semibold text-gray-900">{LastActivityDays} days ago</p>
          </div>
        </div>
      </div>

      {/* Engagement Metrics */}
      <div className="px-6 py-4 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Engagement Metrics</h4>
        <div className="grid grid-cols-3 gap-3 text-center">
          <div>
            <p className="text-xs text-gray-500">Email Opens</p>
            <p className="text-sm font-semibold text-gray-900">{EmailOpens}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Meetings</p>
            <p className="text-sm font-semibold text-gray-900">{MeetingsScheduled}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Calls</p>
            <p className="text-sm font-semibold text-gray-900">{CallsMade}</p>
          </div>
        </div>
      </div>

      {/* Support Issues */}
      {(SupportCases > 0 || CriticalCases > 0) && (
        <div className="px-6 py-4 border-t border-gray-200">
          <div className="flex items-center space-x-2">
            <span className="text-red-500">⚠️</span>
            <span className="text-sm text-gray-700">
              {SupportCases} support cases, {CriticalCases} critical
            </span>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="px-6 py-4 border-t border-gray-200">
        <div className="flex space-x-3">
          <button
            onClick={() => onViewDetails(opportunity)}
            className="flex-1 bg-athena-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-athena-700 transition-colors duration-200"
          >
            View Details
          </button>
          {risk_level?.toLowerCase() !== 'low' && (
            <button
              onClick={() => onRescuePlan(opportunity)}
              className="flex-1 bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 transition-colors duration-200"
            >
              Rescue Plan
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default OpportunityCard;
