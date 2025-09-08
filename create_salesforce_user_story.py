#!/usr/bin/env python3
"""
Script to create actual Salesforce User Stories for AI-Powered Observability Agent incidents
This script demonstrates how to create user stories in Salesforce using the Salesforce REST API
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SalesforceUserStoryCreator:
    def __init__(self):
        self.instance_url = os.getenv('SALESFORCE_INSTANCE_URL', 'https://copadotests-dev-ed.develop.my.salesforce.com')
        self.access_token = os.getenv('SALESFORCE_ACCESS_TOKEN')
        self.session = requests.Session()
        
        if self.access_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            })
    
    def create_user_story(self, incident_data):
        """Create a user story in Salesforce for an incident"""
        try:
            # Prepare user story data
            user_story_data = {
                'Name': f'AI-OBS-{incident_data["id"][:8]}: Code Quality Issues',
                'copado__User_Story_Title__c': f'Resolve Code Quality Issues - Incident {incident_data["id"][:8]}',
                'copado__Description__c': f'''AI-Powered Observability Agent detected code quality issues in PR #{incident_data.get("pr_number", "N/A")}.

Incident Details:
- ID: {incident_data["id"]}
- Severity: {incident_data["severity"]}
- Source: {incident_data["source"]}
- Detected At: {incident_data["detected_at"]}

AI Analysis:
- Root Cause: {incident_data.get("root_cause", "Analysis in progress")}
- Confidence: {incident_data.get("confidence_score", 0) * 100:.1f}%

Actions Taken:
- Automated analysis completed
- PR comment added with detailed findings
- Notifications sent

Next Steps:
- Review AI recommendations
- Implement suggested fixes
- Update code review process
- Monitor for similar issues''',
                'copado__Priority__c': 'High' if incident_data["severity"] in ['critical', 'high'] else 'Medium',
                'copado__Status__c': 'Draft'
            }
            
            # API endpoint for creating user stories
            url = f"{self.instance_url}/services/data/v58.0/sobjects/copado__User_Story__c/"
            
            if not self.access_token:
                print("No Salesforce access token found. Set SALESFORCE_ACCESS_TOKEN in .env file")
                print(f"Would create user story: {user_story_data['copado__User_Story_Title__c']}")
                return {"id": f"demo_{incident_data['id'][:8]}", "success": True}
            
            # Make API call
            response = self.session.post(url, json=user_story_data)
            
            if response.status_code == 201:
                result = response.json()
                print(f"User story created successfully!")
                print(f"Story ID: {result['id']}")
                print(f"Title: {user_story_data['copado__User_Story_Title__c']}")
                return {"id": result['id'], "success": True}
            else:
                print(f"Failed to create user story: {response.status_code}")
                print(f"Response: {response.text}")
                return {"error": response.text, "success": False}
                
        except Exception as e:
            print(f"Error creating user story: {e}")
            return {"error": str(e), "success": False}

def main():
    """Demo function to create user stories for recent incidents"""
    creator = SalesforceUserStoryCreator()
    
    # Example incident data (replace with actual incident data from your system)
    sample_incidents = [
        {
            "id": "bdc7bee1-ecc6-40b8-8bf8-91f84d13d528",
            "severity": "critical",
            "source": "github_pr",
            "pr_number": 4,
            "detected_at": datetime.now().isoformat(),
            "root_cause": "Issue analyzed by Copado AI - DevOps Incident Root Cause Analysis",
            "confidence_score": 0.565
        },
        {
            "id": "13cb3c84-46cd-4ed9-bb44-68f4f9ec00f5",
            "severity": "critical", 
            "source": "github_pr",
            "pr_number": 5,
            "detected_at": datetime.now().isoformat(),
            "root_cause": "Enhanced analysis of github_pr incident with Copado intelligence",
            "confidence_score": 0.565
        }
    ]
    
    print("Creating Salesforce User Stories for AI-Powered Observability Agent incidents...")
    print()
    
    for incident in sample_incidents:
        print(f"Creating user story for incident {incident['id'][:8]}...")
        result = creator.create_user_story(incident)
        print()

if __name__ == "__main__":
    main()
