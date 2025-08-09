import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/Header';
import DashboardContainer from './components/DashboardContainer';
import OpportunityCard from './components/OpportunityCard';
import AlertBanner from './components/AlertBanner';
import { getMockAlerts } from './utils/mockData';
import RescuePlanModal from './components/RescuePlanModal';
import { useMockOpportunity } from './hooks/useAthenaAPI';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const App = () => {
  const [alerts, setAlerts] = useState(getMockAlerts());
  const [selectedOpportunity, setSelectedOpportunity] = useState(null);
  const [isRescueModalOpen, setIsRescueModalOpen] = useState(false);

  const handleDismissAlert = (alertId) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const handleAlertAction = (alert) => {
    console.log('Alert action:', alert);
    // Handle different alert actions
  };

  const handleViewDetails = (opportunity) => {
    console.log('View details for opportunity:', opportunity);
    // Navigate to detailed view or open modal
  };

  const handleRescuePlan = (opportunity) => {
    setSelectedOpportunity(opportunity);
    setIsRescueModalOpen(true);
  };

  const handleSaveRescuePlan = (rescuePlan) => {
    console.log('Saving rescue plan:', rescuePlan);
    // Save to backend or local storage
    // Could also trigger Slack notification here
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Alerts */}
          <div className="mb-6">
            <AlertBanner 
              alerts={alerts}
              onDismiss={handleDismissAlert}
              onAction={handleAlertAction}
            />
          </div>

          {/* Dashboard */}
          <div className="mb-8">
            <DashboardContainer />
          </div>

          {/* Opportunities Grid */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Opportunities</h2>
              <div className="flex space-x-2">
                <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors duration-200">
                  Filter
                </button>
                <button className="px-4 py-2 text-sm font-medium text-white bg-athena-600 border border-transparent rounded-md hover:bg-athena-700 transition-colors duration-200">
                  Add Opportunity
                </button>
              </div>
            </div>
            
            <OpportunitiesGrid 
              onViewDetails={handleViewDetails}
              onRescuePlan={handleRescuePlan}
            />
          </div>
        </main>

        {/* Rescue Plan Modal */}
        <RescuePlanModal
          opportunity={selectedOpportunity}
          isOpen={isRescueModalOpen}
          onClose={() => setIsRescueModalOpen(false)}
          onSave={handleSaveRescuePlan}
        />
      </div>
    </QueryClientProvider>
  );
};

// Opportunities Grid Component
const OpportunitiesGrid = ({ onViewDetails, onRescuePlan }) => {
  const { data: mockOpportunity } = useMockOpportunity();

  // Mock opportunities data
  const mockOpportunities = [
    {
      ...mockOpportunity,
      health_score: 85,
      risk_level: 'Low'
    },
    {
      ...mockOpportunity,
      Id: '006000002',
      Amount: 250000,
      health_score: 45,
      risk_level: 'High',
      DaysInStage: 67,
      LastActivityDays: 12,
      SupportCases: 2,
      CriticalCases: 1
    },
    {
      ...mockOpportunity,
      Id: '006000003',
      Amount: 75000,
      health_score: 62,
      risk_level: 'Medium',
      DaysInStage: 23,
      LastActivityDays: 5
    },
    {
      ...mockOpportunity,
      Id: '006000004',
      Amount: 500000,
      health_score: 78,
      risk_level: 'Low',
      DaysInStage: 15,
      LastActivityDays: 2
    },
    {
      ...mockOpportunity,
      Id: '006000005',
      Amount: 120000,
      health_score: 35,
      risk_level: 'Critical',
      DaysInStage: 89,
      LastActivityDays: 25,
      SupportCases: 3,
      CriticalCases: 2
    },
    {
      ...mockOpportunity,
      Id: '006000006',
      Amount: 180000,
      health_score: 91,
      risk_level: 'Low',
      DaysInStage: 8,
      LastActivityDays: 1
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {mockOpportunities.map((opportunity) => (
        <OpportunityCard
          key={opportunity.Id}
          opportunity={opportunity}
          onViewDetails={onViewDetails}
          onRescuePlan={onRescuePlan}
        />
      ))}
    </div>
  );
};

export default App;
