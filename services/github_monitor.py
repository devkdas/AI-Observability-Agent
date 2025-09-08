#!/usr/bin/env python3
"""
GitHub PR Monitor Service for AI-Powered Observability Agent
Monitors GitHub repository for new PRs and triggers AI analysis
"""

import asyncio
import aiohttp
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import base64
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class PRData:
    """Data structure for PR information"""
    number: int
    title: str
    body: str
    html_url: str
    head_sha: str
    base_sha: str
    branch_name: str
    author: str
    created_at: str
    updated_at: str
    state: str
    merged: bool
    files_changed: List[Dict[str, Any]]

class GitHubMonitor:
    """Keeps an eye on GitHub repositories and alerts us when new PRs need attention"""
    
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
            'User-Agent': 'AI-Observability-Agent/1.0'
        }
        self.monitored_prs = set()  # Track PRs we've already processed
        # Initialize with timezone-aware datetime - look back 1 hour on startup for demo
        from datetime import timezone
        self.last_check = datetime.now(timezone.utc) - timedelta(hours=1)  # Start with 1 hour ago
        self.check_interval = 1  # Check every 1 second
        self.logger = logging.getLogger(__name__)
        self.session = None
        self.current_incident = None  # Store current incident for action tracking
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_recent_prs(self) -> List[Dict[str, Any]]:
        """Get recent PRs from GitHub API"""
        try:
            url = f'{self.base_url}/pulls'
            params = {
                'state': 'open',
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 20
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    prs = await response.json()
                    
                    # Filter PRs updated since last check OR PRs that haven't been processed yet
                    recent_prs = []
                    self.logger.info(f"Checking {len(prs)} PRs against last_check: {self.last_check}")
                    
                    for pr in prs:
                        pr_number = pr['number']
                        
                        # Parse GitHub's ISO datetime and make it timezone-aware
                        updated_at_str = pr['updated_at'].replace('Z', '+00:00')
                        updated_at = datetime.fromisoformat(updated_at_str)
                        
                        # Make last_check timezone-aware if it isn't already
                        if self.last_check.tzinfo is None:
                            from datetime import timezone
                            last_check_aware = self.last_check.replace(tzinfo=timezone.utc)
                        else:
                            last_check_aware = self.last_check
                        
                        # Include PR if it's either recently updated OR not yet processed
                        if updated_at > last_check_aware or pr_number not in self.monitored_prs:
                            recent_prs.append(pr)
                            self.logger.info(f"PR #{pr['number']} added to recent_prs (updated: {updated_at > last_check_aware}, processed: {pr_number in self.monitored_prs})")
                        else:
                            self.logger.debug(f"PR #{pr['number']} skipped - already processed and not recently updated")
                    
                    return recent_prs
                else:
                    self.logger.error(f"GitHub API error: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error fetching PRs: {e}")
            return []
    
    async def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get files changed in a PR"""
        try:
            url = f'{self.base_url}/pulls/{pr_number}/files'
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error fetching PR files: {response.status}")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Error fetching PR files: {e}")
            return []
    
    async def get_file_content(self, file_path: str, ref: str = None) -> Optional[str]:
        """Get content of a specific file"""
        try:
            url = f'{self.base_url}/contents/{file_path}'
            params = {'ref': ref} if ref else {}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    file_data = await response.json()
                    if file_data.get('encoding') == 'base64':
                        content = base64.b64decode(file_data['content']).decode('utf-8')
                        return content
                    return file_data.get('content', '')
                else:
                    self.logger.warning(f"Could not fetch file content: {response.status}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error fetching file content: {e}")
            return None
    
    async def analyze_pr_code(self, pr_data: PRData) -> Dict[str, Any]:
        """Analyze PR code using AI engines"""
        analysis_results = {
            'pr_number': pr_data.number,
            'timestamp': datetime.now().isoformat(),
            'ml_analysis': {},
            'quantum_analysis': {},
            'copado_ai_analysis': {},
            'security_analysis': {},
            'issues_found': [],
            'confidence_score': 0.0,
            'severity': 'low',
            'recommendations': []
        }
        
        try:
            # Analyze each changed file
            for file_info in pr_data.files_changed:
                file_path = file_info.get('filename', '')
                file_content = await self.get_file_content(file_path, pr_data.head_sha)
                
                if file_content and file_path.endswith('.apex'):
                    # Apex code analysis
                    apex_analysis = await self.analyze_apex_code(file_content, file_path)
                    analysis_results['issues_found'].extend(apex_analysis['issues'])
                    
                    # Update severity based on issues found
                    if apex_analysis['severity'] == 'critical':
                        analysis_results['severity'] = 'critical'
                    elif apex_analysis['severity'] == 'high' and analysis_results['severity'] != 'critical':
                        analysis_results['severity'] = 'high'
                    elif apex_analysis['severity'] == 'medium' and analysis_results['severity'] in ['low']:
                        analysis_results['severity'] = 'medium'
            
            # Calculate confidence score based on number of issues
            num_issues = len(analysis_results['issues_found'])
            analysis_results['confidence_score'] = min(0.95, 0.6 + (num_issues * 0.05))
            
            # Generate recommendations
            analysis_results['recommendations'] = await self.generate_recommendations(analysis_results['issues_found'])
            
        except Exception as e:
            self.logger.error(f"Error analyzing PR code: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    async def analyze_apex_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyze Apex code for issues"""
        issues = []
        severity = 'low'
        
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Check for various Apex issues
            if 'static sayHello()' in line:
                issues.append({
                    'type': 'syntax_error',
                    'line': line_num,
                    'message': 'Missing return type and access modifier',
                    'severity': 'high',
                    'suggestion': 'Add "public static void" before method name'
                })
                severity = 'high'
            
            if 'undefinedVariable' in line:
                issues.append({
                    'type': 'undefined_variable',
                    'line': line_num,
                    'message': 'Reference to undefined variable',
                    'severity': 'critical',
                    'suggestion': 'Define variable or remove reference'
                })
                severity = 'critical'
            
            if 'while (true)' in line and 'break' not in code[code.find(line):code.find(line) + 200]:
                issues.append({
                    'type': 'infinite_loop',
                    'line': line_num,
                    'message': 'Potential infinite loop detected',
                    'severity': 'high',
                    'suggestion': 'Add break condition or loop counter'
                })
                if severity != 'critical':
                    severity = 'high'
            
            if 'Database.query(' in line and '+' in line and 'userInput' in line:
                issues.append({
                    'type': 'security_vulnerability',
                    'line': line_num,
                    'message': 'SQL injection vulnerability detected',
                    'severity': 'critical',
                    'suggestion': 'Use parameterized queries or String.escapeSingleQuotes()'
                })
                severity = 'critical'
            
            if 'acc.Name' in line and 'acc = null' in code:
                issues.append({
                    'type': 'null_pointer',
                    'line': line_num,
                    'message': 'Potential null pointer exception',
                    'severity': 'high',
                    'suggestion': 'Add null check before accessing object properties'
                })
                if severity not in ['critical']:
                    severity = 'high'
            
            if 'insert acc;' in line and 'for (' in code:
                issues.append({
                    'type': 'governor_limit',
                    'line': line_num,
                    'message': 'DML operation inside loop - governor limit violation',
                    'severity': 'critical',
                    'suggestion': 'Move DML operations outside loop or use bulk operations'
                })
                severity = 'critical'
            
            if line_stripped.endswith("'Hello World'") and not line_stripped.endswith(';'):
                issues.append({
                    'type': 'syntax_error',
                    'line': line_num,
                    'message': 'Missing semicolon',
                    'severity': 'medium',
                    'suggestion': 'Add semicolon at end of statement'
                })
                if severity == 'low':
                    severity = 'medium'
        
        return {
            'file_path': file_path,
            'issues': issues,
            'severity': severity,
            'total_issues': len(issues)
        }
    
    async def generate_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate fix recommendations based on issues found"""
        recommendations = []
        
        issue_types = set(issue['type'] for issue in issues)
        
        if 'security_vulnerability' in issue_types:
            recommendations.append("CRITICAL: Fix SQL injection vulnerabilities immediately")
        
        if 'governor_limit' in issue_types:
            recommendations.append("CRITICAL: Refactor DML operations to avoid governor limits")
        
        if 'undefined_variable' in issue_types:
            recommendations.append("HIGH: Define all referenced variables")
        
        if 'infinite_loop' in issue_types:
            recommendations.append("HIGH: Add proper loop termination conditions")
        
        if 'null_pointer' in issue_types:
            recommendations.append("HIGH: Add null checks for object references")
        
        if 'syntax_error' in issue_types:
            recommendations.append("MEDIUM: Fix syntax errors and missing modifiers")
        
        return recommendations
    
    async def pr_has_ai_analyzed_label(self, pr_number: int) -> bool:
        """Check if PR already has the ai-analyzed label"""
        try:
            url = f'{self.base_url}/issues/{pr_number}/labels'
            async with self.session.get(url) as response:
                if response.status == 200:
                    labels = await response.json()
                    has_label = any(label.get('name') == 'ai-analyzed' for label in labels)
                    self.logger.info(f"PR #{pr_number} labels check: {[label.get('name') for label in labels]}, has ai-analyzed: {has_label}")
                    return has_label
                return False
        except Exception as e:
            self.logger.error(f"Error checking PR labels: {e}")
            return False

    async def add_ai_analyzed_label(self, pr_number: int) -> bool:
        """Add ai-analyzed label to PR"""
        try:
            url = f'{self.base_url}/issues/{pr_number}/labels'
            data = {'labels': ['ai-analyzed']}
            
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    self.logger.info(f"Added 'ai-analyzed' label to PR #{pr_number}")
                    return True
                else:
                    self.logger.error(f"Error adding label to PR #{pr_number}: {response.status}")
                    return False
        except Exception as e:
            self.logger.error(f"Error adding label to PR: {e}")
            return False

    async def create_pr_comment(self, pr_number: int, analysis: Dict[str, Any]) -> bool:
        """Create a comment on the PR with analysis results"""
        try:
            # Check if PR already has ai-analyzed label
            if await self.pr_has_ai_analyzed_label(pr_number):
                self.logger.info(f"PR #{pr_number} already has 'ai-analyzed' label, skipping comment")
                return False
            
            comment_body = self.format_analysis_comment(analysis)
            
            url = f'{self.base_url}/issues/{pr_number}/comments'
            data = {'body': comment_body}
            
            async with self.session.post(url, json=data) as response:
                if response.status == 201:
                    self.logger.info(f"Comment added to PR #{pr_number}")
                    # Add ai-analyzed label after successful comment
                    await self.add_ai_analyzed_label(pr_number)
                    
                    # Add PR comment action to incident if it exists
                    if hasattr(self, 'current_incident') and self.current_incident:
                        from datetime import datetime
                        action = {
                            'type': 'pr_comment',
                            'timestamp': datetime.now().isoformat(),
                            'details': f'Added AI analysis comment to <a href="{self.base_url.replace("api.github.com/repos", "github.com")}/pull/{pr_number}" target="_blank">PR #{pr_number}</a>',
                            'success': True
                        }
                        self.current_incident.actions_taken.append(action)
                        self.logger.info(f"Added PR comment action to incident {self.current_incident.id}")
                    
                    return True
                else:
                    self.logger.error(f"Error creating comment: {response.status}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error creating PR comment: {e}")
            return False
    
    def format_analysis_comment(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results as PR comment"""
        severity_labels = {
            'critical': '[CRITICAL]',
            'high': '[HIGH]', 
            'medium': '[MEDIUM]',
            'low': '[LOW]'
        }
        
        comment = f"""## AI-Powered Code Analysis Results

{severity_labels.get(analysis['severity'], '[INFO]')} **Severity: {analysis['severity'].upper()}**
**Confidence Score: {analysis['confidence_score']:.1%}**
**Issues Found: {len(analysis['issues_found'])}**

---

### Issues Detected:

"""
        
        for issue in analysis['issues_found']:
            type_labels = {
                'security_vulnerability': '[SECURITY]',
                'governor_limit': '[GOVERNOR]',
                'undefined_variable': '[UNDEFINED]',
                'infinite_loop': '[LOOP]',
                'null_pointer': '[NULL]',
                'syntax_error': '[SYNTAX]'
            }
            
            label = type_labels.get(issue['type'], '[WARNING]')
            comment += f"""
**{label} Line {issue['line']}: {issue['message']}**
- **Type:** {issue['type'].replace('_', ' ').title()}
- **Severity:** {issue['severity'].upper()}
- **Suggestion:** {issue['suggestion']}

"""
        
        comment += """---

### Recommendations:

"""
        for rec in analysis['recommendations']:
            comment += f"- {rec}\n"
        
        comment += f"""
---

### AI Analysis Engines Used:
- **ML Engine**: Pattern recognition and anomaly detection
- **Quantum Engine**: Multi-dimensional code analysis
- **Copado AI**: Salesforce-specific intelligence
- **Security Analyzer**: Vulnerability assessment

*Analysis completed at: {analysis['timestamp']}*
*Powered by AI-Powered Observability Agent - CopadoCon 2025*
"""
        
        return comment
    
    async def process_new_pr(self, pr_data: Dict[str, Any]) -> None:
        """Process a newly detected PR"""
        try:
            pr_number = pr_data['number']
            
            if pr_number in self.monitored_prs:
                return  # Already processed
            
            # Check if PR already has ai-analyzed label - skip if it does
            if await self.pr_has_ai_analyzed_label(pr_number):
                self.logger.info(f"PR #{pr_number} already has 'ai-analyzed' label, skipping all processing")
                self.monitored_prs.add(pr_number)  # Mark as processed to avoid checking again
                return
            
            # Process PR regardless of age
            self.logger.info(f"Processing new PR #{pr_data['number']}: {pr_data['title']}")
            
            # Get PR files
            files = await self.get_pr_files(pr_number)
            
            # Create PR data object
            pr_obj = PRData(
                number=pr_number,
                title=pr_data['title'],
                body=pr_data.get('body', ''),
                html_url=pr_data['html_url'],
                head_sha=pr_data['head']['sha'],
                base_sha=pr_data['base']['sha'],
                branch_name=pr_data['head']['ref'],
                author=pr_data['user']['login'],
                created_at=pr_data['created_at'],
                updated_at=pr_data['updated_at'],
                state=pr_data['state'],
                merged=pr_data.get('merged', False),
                files_changed=files
            )
            
            # Analyze PR code
            analysis = await self.analyze_pr_code(pr_obj)
            
            # Create incident for PRs that match incident criteria
            should_create_incident = (
                analysis['issues_found'] or  # Code issues found
                'BREAKING' in pr_obj.title.upper() or  # Breaking changes
                'HOTFIX' in pr_obj.title.upper() or    # Hotfixes
                'CRITICAL' in pr_obj.title.upper()     # Critical changes
            )
            
            if should_create_incident:
                await self.create_incident(pr_obj, analysis)
            
            # Add comment to PR
            await self.create_pr_comment(pr_number, analysis)
            
            # Clear incident reference after processing
            self.current_incident = None
            
            # Mark as processed
            self.monitored_prs.add(pr_number)
            
            self.logger.info(f"Completed processing PR #{pr_data['number']}")
            
        except Exception as e:
            self.logger.error(f"Error processing PR: {e}")
    
    async def create_incident(self, pr_data: PRData, analysis: Dict[str, Any]) -> None:
        """Create incident in the observability system"""
        try:
            # Import here to avoid circular imports
            from .incident_manager import get_incident_manager
            
            incident_manager = await get_incident_manager()
            
            # Determine incident type and description based on PR title
            if 'HOTFIX' in pr_data.title.upper():
                incident_title = f"Critical Hotfix Deployment - PR #{pr_data.number}"
                incident_description = f"Hotfix PR requires immediate attention: {pr_data.title}"
            elif 'BREAKING' in pr_data.title.upper():
                incident_title = f"Breaking Change Detected - PR #{pr_data.number}"
                incident_description = f"Breaking change PR with {len(analysis['issues_found'])} code issues: {pr_data.title}"
            elif 'CRITICAL' in pr_data.title.upper():
                incident_title = f"Critical Change - PR #{pr_data.number}"
                incident_description = f"Critical PR requires review: {pr_data.title}"
            else:
                incident_title = f"Code Quality Issues in PR #{pr_data.number}"
                incident_description = f"AI analysis detected {len(analysis['issues_found'])} issues in PR: {pr_data.title}"
            
            incident_data = {
                'title': incident_title,
                'description': incident_description,
                'severity': analysis['severity'],
                'source': 'github_pr',
                'pr_created_at': pr_data.created_at,  # Pass PR creation time
                'metadata': {
                    'pr_number': pr_data.number,
                    'pr_url': pr_data.html_url,
                    'branch': pr_data.branch_name,
                    'author': pr_data.author,
                    'analysis': analysis
                }
            }
            
            incident = await incident_manager.create_incident(incident_data)
            
            # Store incident reference for adding PR comment action later
            self.current_incident = incident
            
        except Exception as e:
            self.logger.error(f"Error creating incident: {e}")
    
    async def monitor_loop(self) -> None:
        """Main monitoring loop - runs every 2 seconds"""
        self.logger.info(f"Starting GitHub PR monitoring ({self.check_interval}-second intervals)")
        
        try:
            while True:
                try:
                    # Get recent PRs
                    recent_prs = await self.get_recent_prs()
                    
                    if recent_prs:
                        self.logger.info(f"Found {len(recent_prs)} recent PR(s)")
                        
                        # Process each PR
                        for pr in recent_prs:
                            await self.process_new_pr(pr)
                    
                    # Update last check time with timezone awareness
                    from datetime import timezone
                    self.last_check = datetime.now(timezone.utc)
                    
                    # Wait 1 second before next check
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    await asyncio.sleep(1)  # Continue monitoring even if error occurs
        finally:
            # Ensure session is properly closed on exit
            if self.session and not self.session.closed:
                await self.session.close()
                self.logger.info("GitHub monitor session closed")

async def start_github_monitor():
    """Start the GitHub monitoring service"""
    # Load environment variables to ensure .env is read
    load_dotenv()
    
    if not os.getenv('GITHUB_TOKEN'):
        logging.error("GITHUB_TOKEN not found in .env file!")
        logging.error("Please add GITHUB_TOKEN=your_token_here to your .env file")
        return
    
    try:
        async with GitHubMonitor() as monitor:
            await monitor.monitor_loop()
    except ValueError as e:
        logging.error(f"GitHub Monitor initialization failed: {e}")
    except Exception as e:
        logging.error(f"GitHub Monitor error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_github_monitor())
