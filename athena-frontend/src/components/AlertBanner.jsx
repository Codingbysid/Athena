import React, { useState, useEffect } from 'react';

const AlertBanner = ({ alerts = [], onDismiss, onAction }) => {
  const [visibleAlerts, setVisibleAlerts] = useState([]);

  useEffect(() => {
    setVisibleAlerts(alerts);
  }, [alerts]);

  const getAlertTypeStyles = (type) => {
    switch (type?.toLowerCase()) {
      case 'critical':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          text: 'text-red-800',
          icon: '🚨',
          button: 'bg-red-600 hover:bg-red-700'
        };
      case 'warning':
        return {
          bg: 'bg-yellow-50',
          border: 'border-yellow-200',
          text: 'text-yellow-800',
          icon: '⚠️',
          button: 'bg-yellow-600 hover:bg-yellow-700'
        };
      case 'info':
        return {
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          text: 'text-blue-800',
          icon: 'ℹ️',
          button: 'bg-blue-600 hover:bg-blue-700'
        };
      case 'success':
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          text: 'text-green-800',
          icon: '✅',
          button: 'bg-green-600 hover:bg-green-700'
        };
      default:
        return {
          bg: 'bg-gray-50',
          border: 'border-gray-200',
          text: 'text-gray-800',
          icon: '📢',
          button: 'bg-gray-600 hover:bg-gray-700'
        };
    }
  };

  const handleDismiss = (alertId) => {
    setVisibleAlerts(prev => prev.filter(alert => alert.id !== alertId));
    onDismiss?.(alertId);
  };

  const handleAction = (alert) => {
    onAction?.(alert);
  };

  if (visibleAlerts.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      {visibleAlerts.map((alert) => {
        const styles = getAlertTypeStyles(alert.type);
        
        return (
          <div
            key={alert.id}
            className={`${styles.bg} ${styles.border} border rounded-lg p-4 transition-all duration-200`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <span className="text-lg">{styles.icon}</span>
                <div className="flex-1">
                  <h3 className={`text-sm font-medium ${styles.text}`}>
                    {alert.title}
                  </h3>
                  {alert.message && (
                    <p className={`mt-1 text-sm ${styles.text}`}>
                      {alert.message}
                    </p>
                  )}
                  {alert.details && (
                    <div className="mt-2 text-xs text-gray-600">
                      {alert.details}
                    </div>
                  )}
                  {alert.timestamp && (
                    <div className="mt-1 text-xs text-gray-500">
                      {new Date(alert.timestamp).toLocaleString()}
                    </div>
                  )}
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                {alert.action && (
                  <button
                    onClick={() => handleAction(alert)}
                    className={`${styles.button} text-white px-3 py-1 rounded-md text-xs font-medium transition-colors duration-200`}
                  >
                    {alert.action}
                  </button>
                )}
                <button
                  onClick={() => handleDismiss(alert.id)}
                  className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AlertBanner;
