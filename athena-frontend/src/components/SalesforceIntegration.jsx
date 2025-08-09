import React, { useState } from 'react';

const SalesforceIntegration = ({ opportunity, onSync }) => {
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncStatus, setSyncStatus] = useState('');

  const handleSyncToSalesforce = async () => {
    setIsSyncing(true);
    setSyncStatus('Syncing...');
    
    try {
      // Simulate API call to Salesforce
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock successful sync
      setSyncStatus('✅ Synced successfully');
      onSync?.(opportunity);
      
      setTimeout(() => {
        setSyncStatus('');
        setIsSyncing(false);
      }, 3000);
    } catch {
      setSyncStatus('❌ Sync failed');
      setTimeout(() => {
        setSyncStatus('');
        setIsSyncing(false);
      }, 3000);
    }
  };

  const getSalesforceFields = () => [
    { label: 'Opportunity ID', value: opportunity.Id, type: 'text' },
    { label: 'Account Name', value: 'Acme Corporation', type: 'text' },
    { label: 'Owner', value: 'John Smith', type: 'text' },
    { label: 'Amount', value: `$${opportunity.Amount?.toLocaleString()}`, type: 'currency' },
    { label: 'Stage', value: opportunity.StageName, type: 'picklist' },
    { label: 'Close Date', value: '2024-03-15', type: 'date' },
    { label: 'Probability', value: `${opportunity.health_score || 0}%`, type: 'percentage' },
    { label: 'Lead Source', value: 'Website', type: 'picklist' },
    { label: 'Type', value: 'New Business', type: 'picklist' },
    { label: 'Description', value: 'AI-powered sales intelligence platform', type: 'textarea' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">☁️</span>
          <h3 className="text-lg font-semibold text-gray-900">Salesforce Integration</h3>
        </div>
        <span className="text-sm text-gray-500">Lightning Platform</span>
      </div>

      <div className="space-y-4">
        {/* Salesforce Fields */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Salesforce Fields</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {getSalesforceFields().map((field, index) => (
              <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                <span className="text-sm text-gray-600">{field.label}:</span>
                <span className="text-sm font-medium text-gray-900">{field.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Sync Status */}
        {syncStatus && (
          <div className={`p-3 rounded-lg text-sm font-medium ${
            syncStatus.includes('✅') ? 'bg-green-100 text-green-800' :
            syncStatus.includes('❌') ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {syncStatus}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={handleSyncToSalesforce}
            disabled={isSyncing}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {isSyncing ? 'Syncing...' : 'Sync to Salesforce'}
          </button>
          <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-700 transition-colors duration-200">
            View in Salesforce
          </button>
        </div>

        {/* Integration Status */}
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Integration Status:</span>
            <span className="text-green-600 font-medium">✅ Connected</span>
          </div>
          <div className="flex items-center justify-between text-sm mt-1">
            <span className="text-gray-600">Last Sync:</span>
            <span className="text-gray-900">2 minutes ago</span>
          </div>
          <div className="flex items-center justify-between text-sm mt-1">
            <span className="text-gray-600">API Calls:</span>
            <span className="text-gray-900">1,247 today</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalesforceIntegration;
