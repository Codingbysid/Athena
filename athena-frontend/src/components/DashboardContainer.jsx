import React, { useEffect, useState } from 'react';
import { useAnalytics, useDashboard } from '../hooks/useAthenaAPI';

const DashboardContainer = () => {
  const { data: analyticsData, isLoading: analyticsLoading, error: analyticsError } = useAnalytics();
  const { data: dashboardLoading, error: dashboardError } = useDashboard();
  const [tableauLoaded, setTableauLoaded] = useState(false);

  // Mock Tableau configuration for development
  const tableauConfig = {
    serverUrl: 'https://public.tableau.com',
    siteUrl: '',
    path: '/views/AthenaHealthScores/AthenaDashboard',
    options: {
      hideTabs: true,
      width: '100%',
      height: '600px',
      device: 'desktop'
    }
  };

  useEffect(() => {
    // Load Tableau Embedding API
    const loadTableauAPI = async () => {
      try {
        // In a real implementation, you would load the Tableau Embedding API
        // For now, we'll simulate the loading
        setTimeout(() => {
          setTableauLoaded(true);
        }, 1000);
      } catch (error) {
        console.error('Failed to load Tableau API:', error);
      }
    };

    loadTableauAPI();
  }, []);



  const getMetricCard = (title, value, change, isPositive = true) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        {change && (
          <div className={`flex items-center space-x-1 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            <span className="text-sm font-medium">{isPositive ? '+' : ''}{change}</span>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d={isPositive ? "M5 10l7-7m0 0l7 7m-7-7v18" : "M19 14l-7 7m0 0l-7-7m7 7V3"} />
            </svg>
          </div>
        )}
      </div>
    </div>
  );

  if (analyticsLoading || dashboardLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-athena-600"></div>
      </div>
    );
  }

  if (analyticsError || dashboardError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center space-x-2">
          <span className="text-red-500">❌</span>
          <span className="text-red-700">Failed to load dashboard data</span>
        </div>
      </div>
    );
  }

  // Use mock data if real data is not available
  const data = analyticsData || {
    total_opportunities: 1250,
    average_health_score: 72.5,
    high_risk_opportunities: 89,
    model_performance: {
      auc_score: 0.6968,
      accuracy: 0.85,
      precision: 0.78,
      recall: 0.82
    }
  };

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {getMetricCard(
          'Total Opportunities',
          data.total_opportunities?.toLocaleString() || '1,250',
          '+12%',
          true
        )}
        {getMetricCard(
          'Average Health Score',
          `${data.average_health_score?.toFixed(1) || '72.5'}%`,
          '+5.2%',
          true
        )}
        {getMetricCard(
          'High Risk Opportunities',
          data.high_risk_opportunities || '89',
          '-8%',
          false
        )}
        {getMetricCard(
          'Model AUC Score',
          (data.model_performance?.auc_score * 100)?.toFixed(1) || '69.7',
          '+11.7%',
          true
        )}
      </div>

      {/* Tableau Dashboard */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Health Score Analytics</h2>
          <p className="text-sm text-gray-500">Interactive dashboard powered by Tableau</p>
        </div>
        <div className="p-6">
          {tableauLoaded ? (
            <div className="bg-gray-100 rounded-lg p-8 text-center">
              <div className="text-gray-500 mb-4">
                <svg className="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} 
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p className="text-lg font-medium">Tableau Dashboard</p>
                <p className="text-sm">Embedded Tableau visualization would appear here</p>
                <p className="text-xs text-gray-400 mt-2">
                  Server: {tableauConfig.serverUrl}<br />
                  Path: {tableauConfig.path}
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-athena-600"></div>
              <span className="ml-3 text-gray-600">Loading Tableau dashboard...</span>
            </div>
          )}
        </div>
      </div>

      {/* Model Performance */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Model Performance</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <p className="text-sm text-gray-500">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">
                {((data.model_performance?.accuracy || 0.85) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">Precision</p>
              <p className="text-2xl font-bold text-gray-900">
                {((data.model_performance?.precision || 0.78) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">Recall</p>
              <p className="text-2xl font-bold text-gray-900">
                {((data.model_performance?.recall || 0.82) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">AUC Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {((data.model_performance?.auc_score || 0.6968) * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardContainer;
