import React from 'react';
import { useHealthCheck } from '../hooks/useAthenaAPI';

const Header = () => {
  const { isLoading, error } = useHealthCheck();

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500';
      case 'warning':
        return 'bg-yellow-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'healthy':
        return 'System Healthy';
      case 'warning':
        return 'System Warning';
      case 'error':
        return 'System Error';
      default:
        return 'Unknown Status';
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-gradient-to-r from-athena-500 to-athena-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-sm font-bold">A</span>
              </div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Athena</h1>
              <p className="text-sm text-gray-500">AI Sales Intelligence</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a href="#dashboard" className="text-gray-700 hover:text-athena-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Dashboard
            </a>
            <a href="#opportunities" className="text-gray-700 hover:text-athena-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Opportunities
            </a>
            <a href="#analytics" className="text-gray-700 hover:text-athena-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Analytics
            </a>
            <a href="#models" className="text-gray-700 hover:text-athena-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Models
            </a>
          </nav>

          {/* Status and Actions */}
          <div className="flex items-center space-x-4">
            {/* System Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${getStatusColor(error ? 'error' : isLoading ? 'warning' : 'healthy')}`}></div>
              <span className="text-sm text-gray-600">
                {isLoading ? 'Checking...' : error ? getStatusText('error') : getStatusText('healthy')}
              </span>
            </div>

            {/* User Menu */}
            <div className="relative">
              <button className="flex items-center space-x-2 text-gray-700 hover:text-athena-600 transition-colors">
                <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-gray-700">U</span>
                </div>
                <span className="hidden sm:block text-sm font-medium">User</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button className="md:hidden p-2 rounded-md text-gray-700 hover:text-athena-600 hover:bg-gray-100 transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
