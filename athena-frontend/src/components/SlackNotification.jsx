import React from 'react';

const SlackNotification = ({ opportunity, onSendNotification }) => {
  const generateSlackMessage = (opportunity) => {
    const healthScore = opportunity.health_score || 0;
    const riskLevel = opportunity.risk_level || 'Unknown';

    return {
      text: `🚨 Opportunity Alert: ${opportunity.Id}`,
      blocks: [
        {
          type: "header",
          text: {
            type: "plain_text",
            text: `Opportunity Alert: ${opportunity.Id}`,
            emoji: true
          }
        },
        {
          type: "section",
          fields: [
            {
              type: "mrkdwn",
              text: `*Health Score:*\n${healthScore}%`
            },
            {
              type: "mrkdwn",
              text: `*Risk Level:*\n${riskLevel}`
            },
            {
              type: "mrkdwn",
              text: `*Deal Value:*\n$${opportunity.Amount?.toLocaleString()}`
            },
            {
              type: "mrkdwn",
              text: `*Stage:*\n${opportunity.StageName}`
            }
          ]
        },
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Risk Factors:*\n• ${opportunity.DaysInStage} days in current stage\n• ${opportunity.LastActivityDays} days since last activity\n• ${opportunity.SupportCases || 0} support cases open`
          }
        },
        {
          type: "divider"
        },
        {
          type: "actions",
          elements: [
            {
              type: "button",
              text: {
                type: "plain_text",
                text: "View Details",
                emoji: true
              },
              style: "primary",
              value: opportunity.Id,
              action_id: "view_opportunity"
            },
            {
              type: "button",
              text: {
                type: "plain_text",
                text: "Create Rescue Plan",
                emoji: true
              },
              style: "danger",
              value: opportunity.Id,
              action_id: "create_rescue_plan"
            },
            {
              type: "button",
              text: {
                type: "plain_text",
                text: "Assign to Me",
                emoji: true
              },
              value: opportunity.Id,
              action_id: "assign_opportunity"
            }
          ]
        }
      ]
    };
  };

  const handleSendNotification = () => {
    const message = generateSlackMessage(opportunity);
    onSendNotification(message);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">💬</span>
          <h3 className="text-lg font-semibold text-gray-900">Slack Notification</h3>
        </div>
        <span className="text-sm text-gray-500">Block Kit Format</span>
      </div>

      <div className="space-y-4">
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Message Preview</h4>
          <div className="text-sm text-gray-600 space-y-2">
            <p><strong>Header:</strong> Opportunity Alert: {opportunity.Id}</p>
            <p><strong>Health Score:</strong> {opportunity.health_score || 0}%</p>
            <p><strong>Risk Level:</strong> {opportunity.risk_level || 'Unknown'}</p>
            <p><strong>Deal Value:</strong> ${opportunity.Amount?.toLocaleString()}</p>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Actions</h4>
          <div className="flex space-x-2">
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">View Details</span>
            <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">Create Rescue Plan</span>
            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Assign to Me</span>
          </div>
        </div>

        <button
          onClick={handleSendNotification}
          className="w-full bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors duration-200"
        >
          Send to Slack
        </button>
      </div>
    </div>
  );
};

export default SlackNotification;
