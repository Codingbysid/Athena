/**
 * Athena Opportunity Trigger
 * 
 * This trigger automatically calculates health scores for opportunities
 * and triggers rescue workflows when scores drop below threshold.
 */
trigger AthenaOpportunityTrigger on Opportunity (before insert, before update, after insert, after update) {
    
    // Handle before events for data preparation
    if (Trigger.isBefore) {
        AthenaOpportunityHandler.handleBeforeEvents(Trigger.new, Trigger.oldMap);
    }
    
    // Handle after events for health score calculation and rescue workflows
    if (Trigger.isAfter) {
        AthenaOpportunityHandler.handleAfterEvents(Trigger.new, Trigger.oldMap);
    }
} 