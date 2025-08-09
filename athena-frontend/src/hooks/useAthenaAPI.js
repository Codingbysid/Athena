import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import athenaAPI from '../services/api';

// Health Check Hook
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => athenaAPI.getHealth(),
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  });
};

// Analytics Hook
export const useAnalytics = () => {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: () => athenaAPI.getAnalytics(),
    refetchInterval: 60000, // Refetch every minute
    staleTime: 30000, // Consider data stale after 30 seconds
  });
};

// Models Hook
export const useModels = () => {
  return useQuery({
    queryKey: ['models'],
    queryFn: () => athenaAPI.getModels(),
    staleTime: 300000, // Consider data stale after 5 minutes
  });
};

// Dashboard Hook
export const useDashboard = () => {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: () => athenaAPI.getDashboard(),
    staleTime: 60000, // Consider data stale after 1 minute
  });
};

// Prediction Mutation
export const usePrediction = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (opportunityData) => athenaAPI.predictHealth(opportunityData),
    onSuccess: (data) => {
      // Invalidate and refetch analytics after successful prediction
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      console.log('✅ Prediction successful:', data);
    },
    onError: (error) => {
      console.error('❌ Prediction failed:', error);
    },
  });
};

// Drift Check Mutation
export const useDriftCheck = () => {
  return useMutation({
    mutationFn: (data) => athenaAPI.checkDrift(data),
    onSuccess: (data) => {
      console.log('✅ Drift check successful:', data);
    },
    onError: (error) => {
      console.error('❌ Drift check failed:', error);
    },
  });
};

// Mock Data Hooks for Development
export const useMockAnalytics = () => {
  return useQuery({
    queryKey: ['mock-analytics'],
    queryFn: () => Promise.resolve(athenaAPI.getMockAnalytics()),
    refetchInterval: 60000,
    staleTime: 30000,
  });
};

export const useMockOpportunity = () => {
  return useQuery({
    queryKey: ['mock-opportunity'],
    queryFn: () => Promise.resolve(athenaAPI.getMockOpportunity()),
    staleTime: 300000,
  });
};
