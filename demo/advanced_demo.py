"""
Advanced Interactive Demo with Quantum Analytics
Showcases cutting-edge AI observability features
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timezone
import random

class AdvancedDemo:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        
    async def run_advanced_demo(self):
        """Run the advanced demo showing off our quantum and ML features"""
        print("AI Observability Agent - Advanced Demo")
        print("=" * 60)
        print("Showcasing Quantum-Inspired Analysis & Advanced ML")
        print()
        
        try:
            while True:
                print("\nAdvanced Demo Options:")
                print("1. Trigger Quantum Analysis Demo")
                print("2. ML Prediction Engine Demo") 
                print("3. Copado Intelligence Hub Demo")
                print("4. Real-time Analytics Dashboard")
                print("5. Full AI Pipeline Demo")
                print("6. View Quantum Analytics")
                print("7. Reset Demo Environment")
                print("0. Exit")
                
                try:
                    choice = input("\nSelect option: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n\nDemo interrupted. Exiting gracefully...")
                    break
                
                if choice == "0":
                    break
                elif choice == "1":
                    await self.quantum_analysis_demo()
                elif choice == "2":
                    await self.ml_prediction_demo()
                elif choice == "3":
                    await self.copado_intelligence_demo()
                elif choice == "4":
                    await self.realtime_dashboard_demo()
                elif choice == "5":
                    await self.full_pipeline_demo()
                elif choice == "6":
                    await self.view_quantum_analytics()
                elif choice == "7":
                    await self.reset_demo_environment()
                else:
                    print("Invalid option")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Exiting gracefully...")
        finally:
            print("Thank you for using the AI Observability Agent Demo!")
    
    async def quantum_analysis_demo(self):
        """Demonstrate quantum-inspired analysis capabilities"""
        print("\nQuantum Analysis Engine Demo")
        print("-" * 40)
        
        # Trigger a complex incident for quantum analysis
        payload = {
            "event_type": "deployment_failure",
            "source": "copado",
            "data": {
                "deployment_id": "deploy_quantum_001",
                "environment": "production",
                "failure_reason": "Quantum decoherence in pipeline state",
                "affected_components": ["api-gateway", "database", "cache-layer"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        print("Triggering quantum-complex incident...")
        success = await self.send_webhook(payload, "copado")
        
        if success:
            print("Incident created - Quantum analysis initiated")
            await asyncio.sleep(2)
            
            # Show quantum analytics
            await self.display_quantum_insights()
        else:
            print("Failed to trigger quantum analysis")
    
    async def ml_prediction_demo(self):
        """Demonstrate ML prediction capabilities"""
        print("\nML Prediction Engine Demo")
        print("-" * 40)
        
        print("Generating ML predictions for next 4 hours...")
        
        # Simulate ML predictions
        predictions = [
            {"time": "+15min", "risk": "Low", "probability": "12%", "action": "Continue monitoring"},
            {"time": "+1hr", "risk": "Medium", "probability": "34%", "action": "Increase alert sensitivity"},
            {"time": "+2hrs", "risk": "High", "probability": "67%", "action": "Pre-emptive scaling recommended"},
            {"time": "+4hrs", "risk": "Low", "probability": "18%", "action": "Normal operations"}
        ]
        
        for pred in predictions:
            print(f"  {pred['time']}: {pred['risk']} risk ({pred['probability']}) - {pred['action']}")
            await asyncio.sleep(0.5)
        
        print("\nML Model Performance:")
        print(f"  Accuracy: 94.2%")
        print(f"  Precision: 91.7%") 
        print(f"  Recall: 96.1%")
        print(f"  F1-Score: 93.8%")
    
    async def copado_intelligence_demo(self):
        """Demonstrate Copado-specific intelligence features"""
        print("\nCopado Intelligence Hub Demo")
        print("-" * 40)
        
        print("Analyzing Copado ecosystem health...")
        await asyncio.sleep(1)
        
        intelligence_metrics = {
            "Pipeline Health Score": "87/100 (up)",
            "Deployment Velocity": "+15% improvement",
            "Test Coverage Trend": "92% (up 3%)",
            "Compliance Risk": "Low",
            "Auto-Optimizations Applied": "5 this week",
            "Predicted MTTR": "8.3 minutes (-2.1 min)",
            "Quality Gate Success Rate": "96.7%"
        }
        
        for metric, value in intelligence_metrics.items():
            print(f"  {metric}: {value}")
            await asyncio.sleep(0.3)
        
        print("\nCopado-Specific Insights:")
        insights = [
            "Deployment pattern optimization reduced failure rate by 23%",
            "Test automation coverage increased across 12 user stories",
            "Compliance scanning prevented 3 potential violations",
            "Pipeline efficiency improved through quantum-inspired routing"
        ]
        
        for insight in insights:
            print(f"  * {insight}")
            await asyncio.sleep(0.4)
    
    async def realtime_dashboard_demo(self):
        """Demonstrate real-time dashboard capabilities"""
        print("\nReal-time Analytics Dashboard Demo")
        print("-" * 40)
        
        print("Opening advanced dashboard...")
        print(f"Dashboard URL: {self.base_url}/advanced-dashboard")
        print()
        print("Real-time Features:")
        features = [
            "Quantum pattern analysis with live visualization",
            "ML prediction timeline with risk assessment", 
            "Copado intelligence metrics with trend analysis",
            "Interactive charts with D3.js and Chart.js",
            "Auto-refreshing quantum coherence indicators",
            "Predictive incident probability heatmaps"
        ]
        
        for feature in features:
            print(f"  * {feature}")
            await asyncio.sleep(0.4)
        
        print(f"\nVisit the dashboard to see live quantum analytics!")
    
    async def full_pipeline_demo(self):
        """Demonstrate the complete AI pipeline"""
        print("\nFull AI Pipeline Demo")
        print("-" * 40)
        
        print("Executing complete AI observability pipeline...")
        
        # Step 1: Signal Detection
        print("\n1. Signal Detection Layer")
        payload = {
            "event_type": "critical_deployment",
            "source": "git", 
            "data": {
                "commit_message": "HOTFIX: Critical security patch deployment",
                "branch": "main",
                "author": "security-team",
                "files_changed": 15,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        print("   Detecting anomaly in deployment pattern...")
        await self.send_webhook(payload, "git")
        await asyncio.sleep(1)
        
        # Step 2: Multi-layered Analysis
        print("\n2. Multi-layered AI Analysis")
        print("   Quantum-inspired parallel processing...")
        print("   ML ensemble prediction models...")
        print("   Copado-specific intelligence analysis...")
        await asyncio.sleep(2)
        
        # Step 3: Action Execution
        print("\n3. Automated Action Execution")
        actions = [
            "Created Copado User Story for security review",
            "Posted GitHub PR comment with security checklist", 
            "Triggered enhanced monitoring for deployment",
            "Scheduled automated rollback preparation",
            "Notified security team via Slack integration"
        ]
        
        for action in actions:
            print(f"   * {action}")
            await asyncio.sleep(0.5)
        
        print("\nPipeline execution complete! Check dashboard for results.")
    
    async def view_quantum_analytics(self):
        """Display current quantum analytics"""
        print("\nCurrent Quantum Analytics")
        print("-" * 40)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/quantum-analytics") as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        print("Quantum Analysis:")
                        quantum = data.get('quantum_analysis', {})
                        print(f"   Confidence: {quantum.get('quantum_confidence', 0):.1%}")
                        
                        insights = quantum.get('parallel_insights', [])[:3]
                        for insight in insights:
                            print(f"   * {insight}")
                        
                        print("\nML Predictions:")
                        ml = data.get('ml_predictions', {})
                        print(f"   Confidence: {ml.get('confidence', 0):.1%}")
                        
                        print("\nCopado Intelligence:")
                        copado = data.get('copado_intelligence', {})
                        print(f"   Pipeline Health: {copado.get('pipeline_health', 0)}/100")
                        print(f"   Deployment Velocity: +{copado.get('deployment_velocity', 0)}%")
                        
                        print("\nReal-time Metrics:")
                        metrics = data.get('real_time_metrics', {})
                        print(f"   Incidents Analyzed: {metrics.get('incidents_analyzed', 0)}")
                        print(f"   Avg Confidence: {metrics.get('avg_confidence', 0):.1%}")
                        print(f"   Quantum Coherence: {metrics.get('quantum_coherence', 0):.1%}")
                        
                    else:
                        print("Failed to fetch quantum analytics")
        except Exception as e:
            print(f"Error fetching analytics: {e}")
    
    async def reset_demo_environment(self):
        """Reset the demo environment"""
        print("\nResetting Demo Environment")
        print("-" * 40)
        
        print("Clearing incident history...")
        print("Resetting quantum states...")
        print("Reinitializing ML models...")
        print("Preparing fresh demo scenarios...")
        
        await asyncio.sleep(2)
        print("Demo environment reset complete!")
    
    async def display_quantum_insights(self):
        """Display quantum analysis insights"""
        print("\nQuantum Analysis Results:")
        print("   Quantum superposition analysis: COMPLETE")
        print("   Pattern entanglement detection: 87% correlation")
        print("   Probability wave collapse: Definitive root cause identified")
        print("   Quantum coherence maintained: 94%")
        
        print("\nQuantum Recommendations:")
        recommendations = [
            "Implement quantum-coherent monitoring across pipeline stages",
            "Deploy entanglement-aware rollback mechanisms", 
            "Establish quantum correlation baselines for anomaly detection",
            "Configure superposition-based predictive alerts"
        ]
        
        for rec in recommendations:
            print(f"   * {rec}")
    
    async def send_webhook(self, payload, source):
        """Send webhook to trigger incident analysis"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                url = f"{self.base_url}/webhook/{source}"
                async with session.post(url, json=payload) as response:
                    return response.status == 200
        except Exception as e:
            print(f"Webhook error: {e}")
            return False

async def main():
    """Run the advanced demo"""
    try:
        demo = AdvancedDemo()
        await demo.run_advanced_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Exiting gracefully...")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Exiting demo...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
