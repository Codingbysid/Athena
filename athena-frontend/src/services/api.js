import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:5002'; // Default Athena API port

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Service Class
class AthenaAPIService {
  // Health Check
  async getHealth() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  // Make Prediction
  async predictHealth(opportunityData) {
    try {
      const response = await apiClient.post('/predict', opportunityData);
      return response.data;
    } catch (error) {
      throw new Error(`Prediction failed: ${error.message}`);
    }
  }

  // Get Analytics
  async getAnalytics() {
    try {
      const response = await apiClient.get('/analytics');
      return response.data;
    } catch (error) {
      throw new Error(`Analytics fetch failed: ${error.message}`);
    }
  }

  // Check Model Drift
  async checkDrift(data) {
    try {
      const response = await apiClient.post('/drift', data);
      return response.data;
    } catch (error) {
      throw new Error(`Drift check failed: ${error.message}`);
    }
  }

  // Get Dashboard Data
  async getDashboard() {
    try {
      const response = await apiClient.get('/dashboard');
      return response.data;
    } catch (error) {
      throw new Error(`Dashboard fetch failed: ${error.message}`);
    }
  }

  // Get Model Information
  async getModels() {
    try {
      const response = await apiClient.get('/models');
      return response.data;
    } catch (error) {
      throw new Error(`Models fetch failed: ${error.message}`);
    }
  }

  // Mock data for development/testing
  getMockOpportunity() {
    return {
      Id: "006000001",
      Amount: 150000,
      StageName: "Negotiation",
      Industry: "Technology",
      Region: "North America",
      DaysInStage: 45,
      EmailOpens: 25,
      EmailClicks: 8,
      ContentDownloads: 3,
      MeetingsScheduled: 4,
      CallsMade: 12,
      SupportCases: 1,
      CriticalCases: 0,
      AvgCaseAge: 5,
      CloseDatePushed: 1,
      LastActivityDays: 15,
      CommunicationFrequency: 8
    };
  }

  getMockAnalytics() {
    return {
      total_opportunities: 1250,
      average_health_score: 72.5,
      high_risk_opportunities: 89,
      model_performance: {
        auc_score: 0.6968,
        accuracy: 0.85,
        precision: 0.78,
        recall: 0.82
      },
      recent_predictions: [
        { id: "006000001", health_score: 85, risk_level: "Low", timestamp: "2024-01-15T10:30:00Z" },
        { id: "006000002", health_score: 45, risk_level: "High", timestamp: "2024-01-15T10:25:00Z" },
        { id: "006000003", health_score: 62, risk_level: "Medium", timestamp: "2024-01-15T10:20:00Z" }
      ]
    };
  }
}

// Create singleton instance
const athenaAPI = new AthenaAPIService();

export default athenaAPI;
