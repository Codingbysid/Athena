/**
 * Athena Opportunity Handler
 * 
 * This class handles opportunity processing for the Athena system,
 * including health score calculation and rescue workflow triggers.
 */
public class AthenaOpportunityHandler {
    
    // Configuration constants
    private static final Integer HEALTH_SCORE_THRESHOLD = 40;
    private static final String ATHENA_API_ENDPOINT = 'https://your-athena-api.com/predict';
    private static final String GEMINI_API_ENDPOINT = 'https://your-athena-api.com/diagnose';
    
    /**
     * Handle before events for data preparation
     */
    public static void handleBeforeEvents(List<Opportunity> newOpps, Map<Id, Opportunity> oldOppMap) {
        // Prepare opportunity data for health score calculation
        prepareOpportunityData(newOpps);
    }
    
    /**
     * Handle after events for health score calculation and rescue workflows
     */
    public static void handleAfterEvents(List<Opportunity> newOpps, Map<Id, Opportunity> oldOppMap) {
        // Calculate health scores for new or updated opportunities
        List<Opportunity> opportunitiesToProcess = new List<Opportunity>();
        
        for (Opportunity opp : newOpps) {
            Opportunity oldOpp = oldOppMap != null ? oldOppMap.get(opp.Id) : null;
            
            // Process if this is a new opportunity or if key fields have changed
            if (oldOpp == null || hasKeyChanges(opp, oldOpp)) {
                opportunitiesToProcess.add(opp);
            }
        }
        
        if (!opportunitiesToProcess.isEmpty()) {
            // Calculate health scores
            calculateHealthScores(opportunitiesToProcess);
            
            // Check for rescue workflow triggers
            triggerRescueWorkflows(opportunitiesToProcess, oldOppMap);
        }
    }
    
    /**
     * Prepare opportunity data for health score calculation
     */
    private static void prepareOpportunityData(List<Opportunity> opportunities) {
        // Ensure all required fields are populated
        for (Opportunity opp : opportunities) {
            if (opp.Amount == null) opp.Amount = 0;
            if (opp.StageName == null) opp.StageName = 'Prospecting';
            if (opp.Industry == null) opp.Industry = 'Technology';
            if (opp.Region__c == null) opp.Region__c = 'North America';
            if (opp.LeadSource == null) opp.LeadSource = 'Website';
        }
    }
    
    /**
     * Check if key fields have changed that would affect health score
     */
    private static Boolean hasKeyChanges(Opportunity newOpp, Opportunity oldOpp) {
        return newOpp.Amount != oldOpp.Amount ||
               newOpp.StageName != oldOpp.StageName ||
               newOpp.Industry != oldOpp.Industry ||
               newOpp.Region__c != oldOpp.Region__c ||
               newOpp.LeadSource != oldOpp.LeadSource ||
               newOpp.CloseDate != oldOpp.CloseDate;
    }
    
    /**
     * Calculate health scores for opportunities using Athena API
     */
    private static void calculateHealthScores(List<Opportunity> opportunities) {
        List<Opportunity> opportunitiesToUpdate = new List<Opportunity>();
        
        for (Opportunity opp : opportunities) {
            try {
                // Prepare data for API call
                Map<String, Object> opportunityData = prepareOpportunityDataForAPI(opp);
                
                // Call Athena API for health score
                Map<String, Object> apiResponse = callAthenaAPI(opportunityData);
                
                if (apiResponse != null && apiResponse.containsKey('health_score')) {
                    Integer healthScore = (Integer) apiResponse.get('health_score');
                    String riskLevel = (String) apiResponse.get('risk_level');
                    
                    // Update opportunity with health score
                    opp.Opportunity_Health_Score__c = healthScore;
                    opp.Risk_Level__c = riskLevel;
                    opp.Last_Health_Score_Calculation__c = Datetime.now();
                    
                    opportunitiesToUpdate.add(opp);
                    
                    // Log the calculation
                    System.debug('Athena: Calculated health score ' + healthScore + ' for opportunity ' + opp.Id);
                }
                
            } catch (Exception e) {
                System.debug('Athena: Error calculating health score for opportunity ' + opp.Id + ': ' + e.getMessage());
                // Continue processing other opportunities
            }
        }
        
        // Update opportunities with health scores
        if (!opportunitiesToUpdate.isEmpty()) {
            try {
                update opportunitiesToUpdate;
            } catch (Exception e) {
                System.debug('Athena: Error updating opportunities with health scores: ' + e.getMessage());
            }
        }
    }
    
    /**
     * Prepare opportunity data for API call
     */
    private static Map<String, Object> prepareOpportunityDataForAPI(Opportunity opp) {
        Map<String, Object> data = new Map<String, Object>();
        
        data.put('Id', opp.Id);
        data.put('Amount', opp.Amount != null ? opp.Amount : 0);
        data.put('StageName', opp.StageName);
        data.put('Industry', opp.Industry);
        data.put('Region', opp.Region__c);
        data.put('LeadSource', opp.LeadSource);
        data.put('DaysInStage', opp.Days_in_Stage__c != null ? opp.Days_in_Stage__c : 0);
        data.put('EmailOpens', opp.Email_Opens__c != null ? opp.Email_Opens__c : 0);
        data.put('EmailClicks', opp.Email_Clicks__c != null ? opp.Email_Clicks__c : 0);
        data.put('ContentDownloads', opp.Content_Downloads__c != null ? opp.Content_Downloads__c : 0);
        data.put('MeetingsScheduled', opp.Meetings_Scheduled__c != null ? opp.Meetings_Scheduled__c : 0);
        data.put('CallsMade', opp.Calls_Made__c != null ? opp.Calls_Made__c : 0);
        data.put('SupportCases', opp.Support_Cases__c != null ? opp.Support_Cases__c : 0);
        data.put('CriticalCases', opp.Critical_Cases__c != null ? opp.Critical_Cases__c : 0);
        data.put('AvgCaseAge', opp.Avg_Case_Age__c != null ? opp.Avg_Case_Age__c : 0);
        data.put('CloseDatePushed', opp.Close_Date_Pushed__c != null ? opp.Close_Date_Pushed__c : 0);
        data.put('LastActivityDays', opp.Last_Activity_Days__c != null ? opp.Last_Activity_Days__c : 0);
        data.put('CommunicationFrequency', opp.Communication_Frequency__c != null ? opp.Communication_Frequency__c : 0);
        
        return data;
    }
    
    /**
     * Call Athena API for health score prediction
     */
    private static Map<String, Object> callAthenaAPI(Map<String, Object> opportunityData) {
        try {
            // Create HTTP request
            Http http = new Http();
            HttpRequest request = new HttpRequest();
            request.setEndpoint(ATHENA_API_ENDPOINT);
            request.setMethod('POST');
            request.setHeader('Content-Type', 'application/json');
            request.setHeader('Authorization', 'Bearer ' + getAthenaAPIToken());
            request.setBody(JSON.serialize(opportunityData));
            
            // Send request
            HttpResponse response = http.send(request);
            
            if (response.getStatusCode() == 200) {
                Map<String, Object> responseData = (Map<String, Object>) JSON.deserializeUntyped(response.getBody());
                return responseData;
            } else {
                System.debug('Athena: API call failed with status ' + response.getStatusCode() + ': ' + response.getBody());
                return null;
            }
            
        } catch (Exception e) {
            System.debug('Athena: Error calling API: ' + e.getMessage());
            return null;
        }
    }
    
    /**
     * Get Athena API authentication token
     */
    private static String getAthenaAPIToken() {
        // This would typically retrieve a token from a custom setting or named credential
        // For demo purposes, return a placeholder
        return 'your-api-token-here';
    }
    
    /**
     * Trigger rescue workflows for opportunities with low health scores
     */
    private static void triggerRescueWorkflows(List<Opportunity> opportunities, Map<Id, Opportunity> oldOppMap) {
        List<Opportunity> opportunitiesNeedingRescue = new List<Opportunity>();
        
        for (Opportunity opp : opportunities) {
            Opportunity oldOpp = oldOppMap != null ? oldOppMap.get(opp.Id) : null;
            
            // Check if health score is below threshold and has decreased
            if (opp.Opportunity_Health_Score__c != null && 
                opp.Opportunity_Health_Score__c < HEALTH_SCORE_THRESHOLD) {
                
                // If this is a new opportunity or the score has decreased
                if (oldOpp == null || 
                    (oldOpp.Opportunity_Health_Score__c != null && 
                     opp.Opportunity_Health_Score__c < oldOpp.Opportunity_Health_Score__c)) {
                    
                    opportunitiesNeedingRescue.add(opp);
                }
            }
        }
        
        if (!opportunitiesNeedingRescue.isEmpty()) {
            createRescuePlans(opportunitiesNeedingRescue);
            sendSlackNotifications(opportunitiesNeedingRescue);
        }
    }
    
    /**
     * Create rescue plan records for at-risk opportunities
     */
    private static void createRescuePlans(List<Opportunity> opportunities) {
        List<Rescue_Plan__c> rescuePlans = new List<Rescue_Plan__c>();
        
        for (Opportunity opp : opportunities) {
            Rescue_Plan__c rescuePlan = new Rescue_Plan__c();
            rescuePlan.Opportunity__c = opp.Id;
            rescuePlan.Health_Score__c = opp.Opportunity_Health_Score__c;
            rescuePlan.Risk_Level__c = opp.Risk_Level__c;
            rescuePlan.Status__c = 'Active';
            rescuePlan.Created_Date__c = Datetime.now();
            rescuePlan.OwnerId = opp.OwnerId;
            
            rescuePlans.add(rescuePlan);
        }
        
        if (!rescuePlans.isEmpty()) {
            try {
                insert rescuePlans;
                System.debug('Athena: Created ' + rescuePlans.size() + ' rescue plans');
            } catch (Exception e) {
                System.debug('Athena: Error creating rescue plans: ' + e.getMessage());
            }
        }
    }
    
    /**
     * Send Slack notifications for at-risk opportunities
     */
    private static void sendSlackNotifications(List<Opportunity> opportunities) {
        for (Opportunity opp : opportunities) {
            try {
                // Prepare Slack message
                Map<String, Object> slackMessage = new Map<String, Object>();
                slackMessage.put('channel', '#deal-rescue-room');
                slackMessage.put('text', '🚨 *Athena Alert: At-Risk Opportunity Detected*');
                
                // Create attachments
                List<Map<String, Object>> attachments = new List<Map<String, Object>>();
                Map<String, Object> attachment = new Map<String, Object>();
                attachment.put('color', '#ff0000');
                attachment.put('title', opp.Name);
                attachment.put('title_link', URL.getSalesforceBaseUrl().toExternalForm() + '/' + opp.Id);
                
                List<Map<String, Object>> fields = new List<Map<String, Object>>();
                
                Map<String, Object> healthScoreField = new Map<String, Object>();
                healthScoreField.put('title', 'Health Score');
                healthScoreField.put('value', opp.Opportunity_Health_Score__c + '/100');
                healthScoreField.put('short', true);
                fields.add(healthScoreField);
                
                Map<String, Object> riskLevelField = new Map<String, Object>();
                riskLevelField.put('title', 'Risk Level');
                riskLevelField.put('value', opp.Risk_Level__c);
                riskLevelField.put('short', true);
                fields.add(riskLevelField);
                
                Map<String, Object> stageField = new Map<String, Object>();
                stageField.put('title', 'Stage');
                stageField.put('value', opp.StageName);
                stageField.put('short', true);
                fields.add(stageField);
                
                Map<String, Object> amountField = new Map<String, Object>();
                amountField.put('title', 'Deal Size');
                amountField.put('value', '$' + opp.Amount.format());
                amountField.put('short', true);
                fields.add(amountField);
                
                attachment.put('fields', fields);
                attachments.add(attachment);
                
                slackMessage.put('attachments', attachments);
                
                // Send to Slack (this would use a callout to Slack API)
                sendSlackMessage(slackMessage);
                
            } catch (Exception e) {
                System.debug('Athena: Error sending Slack notification for opportunity ' + opp.Id + ': ' + e.getMessage());
            }
        }
    }
    
    /**
     * Send message to Slack
     */
    private static void sendSlackMessage(Map<String, Object> message) {
        try {
            // This would make a callout to Slack API
            // For demo purposes, just log the message
            System.debug('Athena: Slack message would be sent: ' + JSON.serialize(message));
            
        } catch (Exception e) {
            System.debug('Athena: Error sending Slack message: ' + e.getMessage());
        }
    }
} 