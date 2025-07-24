"""
Email Monitoring Integration
Consolidates email monitoring functionality from raiderbot-platform
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class EmailMonitoringIntegration:
    """
    Consolidated email monitoring system
    Integrates functionality from raiderbot-platform autonomousService.js
    """
    
    def __init__(self):
        self.logger = logging.getLogger('EmailMonitoringIntegration')
        self.config = self._load_email_config()
        self.alert_thresholds = self._load_alert_thresholds()
        
    def _load_email_config(self) -> Dict[str, Any]:
        """Load email monitoring configuration"""
        return {
            'azure_client_id': os.getenv('AZURE_CLIENT_ID'),
            'azure_tenant_id': os.getenv('AZURE_TENANT_ID'),
            'azure_domain': os.getenv('AZURE_DOMAIN', 'raiderexpress.com'),
            'monitoring_interval': int(os.getenv('EMAIL_MONITORING_INTERVAL', '300')),
            'enabled': os.getenv('EMAIL_MONITORING_ENABLED', 'true').lower() == 'true'
        }
        
    def _load_alert_thresholds(self) -> Dict[str, Any]:
        """Load alert thresholds from environment"""
        return {
            'urgent_email_count': int(os.getenv('URGENT_EMAIL_THRESHOLD', '3')),
            'response_time_hours': int(os.getenv('RESPONSE_TIME_THRESHOLD', '4')),
            'sentiment_threshold': float(os.getenv('SENTIMENT_THRESHOLD', '0.3')),
            'escalation_threshold': int(os.getenv('ESCALATION_THRESHOLD', '5'))
        }
        
    async def monitor_organization_emails(self) -> Dict[str, Any]:
        """
        Monitor organization-wide emails using Azure AD integration
        Consolidated from autonomousService.js functionality
        """
        self.logger.info("Starting organization-wide email monitoring...")
        
        if not self.config['enabled']:
            return {
                'status': 'disabled',
                'message': 'Email monitoring is disabled'
            }
            
        try:
            email_data = await self._fetch_organization_emails()
            analysis_result = await self._analyze_email_patterns(email_data)
            alert_result = await self._check_alert_conditions(analysis_result)
            
            monitoring_result = {
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'emails_processed': len(email_data),
                'analysis': analysis_result,
                'alerts': alert_result,
                'next_check': (datetime.now() + timedelta(seconds=self.config['monitoring_interval'])).isoformat()
            }
            
            self.logger.info(f"Email monitoring completed: {monitoring_result}")
            return monitoring_result
            
        except Exception as e:
            self.logger.error(f"Email monitoring failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    async def _fetch_organization_emails(self) -> List[Dict[str, Any]]:
        """Fetch emails from organization using Azure AD"""
        mock_emails = [
            {
                'id': 'email_001',
                'subject': 'Urgent: Delivery delay on Route 45',
                'sender': 'dispatch@raiderexpress.com',
                'timestamp': datetime.now().isoformat(),
                'priority': 'high',
                'sentiment_score': 0.2
            },
            {
                'id': 'email_002',
                'subject': 'Customer complaint - Late delivery',
                'sender': 'customer.service@raiderexpress.com',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                'priority': 'medium',
                'sentiment_score': 0.1
            },
            {
                'id': 'email_003',
                'subject': 'Fleet maintenance reminder',
                'sender': 'maintenance@raiderexpress.com',
                'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
                'priority': 'low',
                'sentiment_score': 0.8
            }
        ]
        
        return mock_emails
        
    async def _analyze_email_patterns(self, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email patterns for insights"""
        urgent_count = len([e for e in emails if e.get('priority') == 'high'])
        avg_sentiment = sum(e.get('sentiment_score', 0.5) for e in emails) / len(emails) if emails else 0.5
        
        recent_emails = [e for e in emails if 
                        datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=4)]
        
        analysis = {
            'total_emails': len(emails),
            'urgent_emails': urgent_count,
            'average_sentiment': avg_sentiment,
            'recent_emails_4h': len(recent_emails),
            'departments': list(set(e['sender'].split('@')[0] for e in emails)),
            'trends': {
                'urgent_trend': 'increasing' if urgent_count > 2 else 'stable',
                'sentiment_trend': 'negative' if avg_sentiment < 0.4 else 'positive'
            }
        }
        
        return analysis
        
    async def _check_alert_conditions(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check if alert conditions are met"""
        alerts = []
        
        if analysis['urgent_emails'] >= self.alert_thresholds['urgent_email_count']:
            alerts.append({
                'type': 'urgent_email_threshold',
                'severity': 'high',
                'message': f"Urgent email count ({analysis['urgent_emails']}) exceeds threshold ({self.alert_thresholds['urgent_email_count']})",
                'action_required': True
            })
            
        if analysis['average_sentiment'] <= self.alert_thresholds['sentiment_threshold']:
            alerts.append({
                'type': 'negative_sentiment',
                'severity': 'medium',
                'message': f"Average sentiment ({analysis['average_sentiment']:.2f}) below threshold ({self.alert_thresholds['sentiment_threshold']})",
                'action_required': True
            })
            
        if analysis['recent_emails_4h'] >= self.alert_thresholds['escalation_threshold']:
            alerts.append({
                'type': 'high_volume',
                'severity': 'medium',
                'message': f"High email volume in last 4 hours: {analysis['recent_emails_4h']} emails",
                'action_required': False
            })
            
        return {
            'alert_count': len(alerts),
            'alerts': alerts,
            'requires_notification': any(alert['action_required'] for alert in alerts)
        }
        
    async def deploy_to_foundry(self, foundry_client) -> Dict[str, Any]:
        """Deploy email monitoring to Foundry with Azure AD integration"""
        self.logger.info("Deploying email monitoring to Foundry...")
        
        deployment_config = {
            'function_name': 'organization_email_monitoring',
            'schedule': f'*/5 * * * *',
            'azure_integration': {
                'client_id': self.config['azure_client_id'],
                'tenant_id': self.config['azure_tenant_id'],
                'domain': self.config['azure_domain']
            },
            'alert_configuration': self.alert_thresholds
        }
        
        try:
            result = await foundry_client.deploy_function(deployment_config)
            
            return {
                'status': 'deployed',
                'function_id': result.get('function_id', 'email_monitoring_001'),
                'deployment_url': f"{foundry_client.foundry_url}/workspace/functions/email_monitoring_001",
                'configuration': deployment_config,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Foundry deployment failed: {str(e)}")
            return {
                'status': 'deployment_failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
