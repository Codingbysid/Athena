// Mock alerts for development
export const getMockAlerts = () => [
  {
    id: '1',
    type: 'critical',
    title: 'High Risk Opportunity Detected',
    message: 'Opportunity 006000002 has dropped to 45% health score and requires immediate attention.',
    details: 'Deal value: $250,000 | Days in stage: 67 | Last activity: 12 days ago',
    timestamp: new Date().toISOString(),
    action: 'View Details'
  },
  {
    id: '2',
    type: 'warning',
    title: 'Model Drift Detected',
    message: 'Recent predictions show 8% deviation from expected patterns.',
    details: 'Recommendation: Retrain model within 48 hours',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    action: 'Review'
  },
  {
    id: '3',
    type: 'info',
    title: 'System Update',
    message: 'Athena AI model has been updated with latest training data.',
    details: 'New features: 48 engineered features, Ensemble model (XGBoost + LightGBM)',
    timestamp: new Date(Date.now() - 7200000).toISOString(),
    action: 'Learn More'
  }
];
