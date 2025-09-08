#!/usr/bin/env python3
"""
GitHub PR Creation Script for CopadoCon 2025 AI Observability Demo
Creates a PR with intentionally broken Apex code to trigger incident detection
"""

import os
import requests
import json
from datetime import datetime
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GitHubPRCreator:
    def __init__(self):
        # Load GitHub token from .env file
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN not found in .env file. Please add it to your .env file.")
        
        self.repo_owner = 'devkdas'
        self.repo_name = 'Copado-CopadoHack2025SFP'
        self.base_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}'
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
    
    def create_broken_apex_code(self):
        """Generate intentionally broken Apex code with multiple issues"""
        broken_apex = '''public class HelloWorld {
    // INTENTIONAL BUGS FOR AI DETECTION:
    
    // Bug 1: Missing access modifier and return type (Line 5)
    static sayHello() {
        System.debug('Hello World');
    }
    
    // Bug 2: Undefined variable reference (Line 10)
    public static void processData() {
        String result = undefinedVariable.toString();
        System.debug(result);
    }
    
    // Bug 3: Infinite loop potential (Line 15)
    public static void infiniteLoop() {
        while (true) {
            System.debug('This will run forever');
            // Missing break condition
        }
    }
    
    // Bug 4: SQL Injection vulnerability (Line 23)
    public static List<Account> getAccounts(String userInput) {
        String query = 'SELECT Id, Name FROM Account WHERE Name = \\'' + userInput + '\\'';
        return Database.query(query);
    }
    
    // Bug 5: Null pointer exception (Line 29)
    public static void processAccount() {
        Account acc = null;
        String name = acc.Name; // Will throw NullPointerException
        System.debug(name);
    }
    
    // Bug 6: Governor limit violation (Line 35)
    public static void bulkOperation() {
        for (Integer i = 0; i < 50000; i++) {
            Account acc = new Account(Name = 'Test ' + i);
            insert acc; // DML inside loop - governor limit violation
        }
    }
    
    // Bug 7: Incorrect syntax (Line 42)
    public static void syntaxError() {
        String message = 'Hello World'  // Missing semicolon
        System.debug(message);
    }
}'''
        return broken_apex
    
    def get_file_sha(self, file_path):
        """Get the SHA of existing file for updates"""
        try:
            url = f'{self.base_url}/contents/{file_path}'
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()['sha']
            return None
        except Exception as e:
            print(f"Error getting file SHA: {e}")
            return None
    
    def create_or_update_file(self, file_path, content, commit_message, branch_name):
        """Create or update file in repository"""
        try:
            # Encode content to base64
            content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            # Check if file exists
            existing_sha = self.get_file_sha(file_path)
            
            # Prepare request data
            data = {
                'message': commit_message,
                'content': content_encoded,
                'branch': branch_name
            }
            
            if existing_sha:
                data['sha'] = existing_sha
            
            url = f'{self.base_url}/contents/{file_path}'
            response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                print(f"File {file_path} {'updated' if existing_sha else 'created'} successfully")
                return True
            else:
                print(f"Error creating/updating file: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Exception creating/updating file: {e}")
            return False
    
    def create_branch(self, branch_name):
        """Create a new branch from main"""
        try:
            # Get main branch SHA
            main_ref_url = f'{self.base_url}/git/refs/heads/main'
            response = requests.get(main_ref_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error getting main branch: {response.status_code}")
                return False
            
            main_sha = response.json()['object']['sha']
            
            # Create new branch
            create_ref_url = f'{self.base_url}/git/refs'
            data = {
                'ref': f'refs/heads/{branch_name}',
                'sha': main_sha
            }
            
            response = requests.post(create_ref_url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                print(f"Branch '{branch_name}' created successfully")
                return True
            elif response.status_code == 422:
                print(f"Branch '{branch_name}' already exists")
                return True
            else:
                print(f"Error creating branch: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Exception creating branch: {e}")
            return False
    
    def create_pull_request(self, branch_name, title, body):
        """Create a pull request"""
        try:
            url = f'{self.base_url}/pulls'
            data = {
                'title': title,
                'body': body,
                'head': branch_name,
                'base': 'main'
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                pr_data = response.json()
                print(f"Pull Request created successfully!")
                print(f"PR URL: {pr_data['html_url']}")
                print(f"PR Number: {pr_data['number']}")
                return pr_data
            else:
                print(f"Error creating PR: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception creating PR: {e}")
            return None
    
    def run(self):
        """Execute the complete PR creation workflow"""
        if not self.github_token:
            print("GITHUB_TOKEN not found in .env file!")
            print("Please add GITHUB_TOKEN=your_token_here to your .env file")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"ai-observability-test-{timestamp}"
        file_path = "scripts/apex/hello.apex"
        
        print("Starting GitHub PR Creation for AI Observability Demo")
        print(f"Repository: {self.repo_owner}/{self.repo_name}")
        print(f"Target file: {file_path}")
        print(f"Branch: {branch_name}")
        print("-" * 60)
        
        # Step 1: Create branch
        if not self.create_branch(branch_name):
            return False
        
        # Step 2: Create broken Apex code
        broken_code = self.create_broken_apex_code()
        
        # Step 3: Create/update file with broken code
        commit_message = f"Add broken Apex code for AI observability testing - {timestamp}"
        if not self.create_or_update_file(file_path, broken_code, commit_message, branch_name):
            return False
        
        # Step 4: Create pull request
        pr_title = f"BREAKING: Add HelloWorld Apex class with multiple issues"
        pr_body = f"""## AI Observability Test PR - {timestamp}

**WARNING: This PR intentionally contains broken code for testing purposes**

### Changes Made:
- Added `scripts/apex/hello.apex` with HelloWorld class
- **INTENTIONAL BUGS INCLUDED FOR AI DETECTION:**

### Known Issues (for AI to detect):
1. **Line 5**: Missing return type and access modifier
2. **Line 10**: Undefined variable reference
3. **Line 15**: Potential infinite loop
4. **Line 23**: SQL injection vulnerability
5. **Line 29**: Null pointer exception risk
6. **Line 35**: Governor limit violation (DML in loop)
7. **Line 42**: Missing semicolon syntax error

### Expected AI Behavior:
- Our AI Observability Agent should detect this PR
- ML Engine should analyze code quality issues
- Quantum Engine should identify security vulnerabilities
- Copado AI should provide detailed analysis
- System should create incident and suggest fixes
- Auto-comment or auto-fix PR should be generated

### Testing Objectives:
- Validate real-time GitHub PR monitoring
- Test multi-engine AI analysis pipeline
- Verify automated incident creation and resolution
- Demonstrate end-to-end observability workflow

---
*This PR is part of the CopadoCon 2025 AI-Powered Observability Agent demonstration.*
*Created by: AI Observability Test Suite*
*Timestamp: {timestamp}*
"""
        
        pr_data = self.create_pull_request(branch_name, pr_title, pr_body)
        
        if pr_data:
            print("\n" + "=" * 60)
            print("SUCCESS! Breaking PR Created Successfully")
            print("=" * 60)
            print(f"PR URL: {pr_data['html_url']}")
            print(f"PR Number: #{pr_data['number']}")
            print(f"Branch: {branch_name}")
            print(f"File: {file_path}")
            print("\nYour AI Observability Agent should now:")
            print("   1. Detect this new PR within 15 seconds")
            print("   2. Analyze code with ML + Quantum + Copado AI engines")
            print("   3. Create incident in dashboard")
            print("   4. Generate automated fix suggestions")
            print("   5. Post comment with line-by-line issues")
            print("   6. Create Slack notification and Jira user story")
            print("\nMonitor your dashboard at: http://localhost:8000/advanced-dashboard")
            return True
        
        return False

def main():
    """Main execution function"""
    print("CopadoCon 2025 - AI Observability Breaking PR Creator")
    print("=" * 60)
    
    creator = GitHubPRCreator()
    success = creator.run()
    
    if success:
        print("\nBreaking PR created successfully!")
        print("Watch your AI Observability Agent dashboard for real-time incident detection!")
    else:
        print("\nFailed to create breaking PR")
        print("Please check your GitHub token and repository access")

if __name__ == "__main__":
    main()
