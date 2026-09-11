#!/usr/bin/env python3
"""
Telegram CRM Report Bot Handler
Handles /crm_report, /crm_contacts, /crm_leads, /crm_projects commands
"""

import os
import sys
import json
from pathlib import Path

# Add skill scripts to path
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

try:
    from crm_report import (
        generate_full_report,
        generate_mock_report,
        fetch_contacts,
        fetch_leads,
        fetch_accounts,
        analyze_contacts,
        analyze_leads,
        analyze_accounts
    )
except ImportError as e:
    print(f"Error importing crm_report: {e}")
    sys.exit(1)


def format_telegram_message(report_data: dict) -> str:
    """Format report for Telegram display"""
    
    if isinstance(report_data, str):
        # Already formatted
        return report_data
    
    # Extract analysis
    analysis = report_data.get('analysis', {})
    contacts = analysis.get('contacts', {})
    leads = analysis.get('leads', {})
    accounts = analysis.get('accounts', {})
    
    # Build message
    msg = "*CRM ANALYTICS REPORT*\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    msg += f"📊 *CONTACTS*\n"
    msg += f"Total: {contacts.get('total', 0)}\n"
    msg += f"Active: {contacts.get('by_status', {}).get('Active', 0)}\n"
    msg += f"Inactive: {contacts.get('by_status', {}).get('Inactive', 0)}\n"
    msg += f"Active Rate: {contacts.get('percentage_active', 0)}%\n\n"
    
    msg += f"💼 *ACCOUNTS*\n"
    msg += f"Total: {accounts.get('total', 0)}\n"
    msg += f"Revenue: Rs {accounts.get('total_revenue', 0):,.0f}\n"
    msg += f"Avg: Rs {accounts.get('avg_revenue', 0):,.0f}\n\n"
    
    msg += f"🎯 *LEADS PIPELINE*\n"
    msg += f"Total Deals: {leads.get('total', 0)}\n"
    msg += f"Pipeline Value: Rs {leads.get('pipeline_value', 0):,.0f}\n"
    msg += f"Win Rate: {leads.get('win_rate', 0)}%\n\n"
    
    msg += "*By Stage:*\n"
    for stage, count in leads.get('by_stage', {}).items():
        value = leads.get('by_stage_value', {}).get(stage, 0)
        msg += f"  {stage}: {count} (Rs {value:,.0f})\n"
    
    return msg


def handle_crm_report(report_type: str = 'full') -> dict:
    """
    Handle CRM report generation
    
    Args:
        report_type: 'full', 'contacts', 'leads', or 'projects'
    
    Returns:
        Dictionary with 'success', 'message', and 'data' keys
    """
    
    try:
        # Generate report with analysis
        report = generate_full_report('text')
        
        if not report.get('success'):
            return {
                'success': False,
                'message': 'Failed to generate report',
                'error': 'Unknown error'
            }
        
        # Build Telegram message from analysis
        analysis = report.get('analysis', {})
        contacts = analysis.get('contacts', {})
        leads = analysis.get('leads', {})
        accounts = analysis.get('accounts', {})
        
        msg = "*CRM ANALYTICS REPORT*\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        msg += f"📊 *CONTACTS*\n"
        msg += f"Total: {contacts.get('total', 0)}\n"
        msg += f"Active: {contacts.get('by_status', {}).get('Active', 0)}\n"
        msg += f"Inactive: {contacts.get('by_status', {}).get('Inactive', 0)}\n"
        msg += f"Active Rate: {contacts.get('percentage_active', 0)}%\n\n"
        
        msg += f"💼 *ACCOUNTS*\n"
        msg += f"Total: {accounts.get('total', 0)}\n"
        msg += f"Revenue: Rs {accounts.get('total_revenue', 0):,.0f}\n"
        msg += f"Avg: Rs {accounts.get('avg_revenue', 0):,.0f}\n\n"
        
        msg += f"🎯 *LEADS PIPELINE*\n"
        msg += f"Total Deals: {leads.get('total', 0)}\n"
        msg += f"Pipeline Value: Rs {leads.get('pipeline_value', 0):,.0f}\n"
        msg += f"Win Rate: {leads.get('win_rate', 0)}%\n\n"
        
        msg += "*By Stage:*\n"
        for stage, count in leads.get('by_stage', {}).items():
            value = leads.get('by_stage_value', {}).get(stage, 0)
            msg += f"  {stage}: {count} (Rs {value:,.0f})\n"
        
        return {
            'success': True,
            'message': msg,
            'analysis': analysis,
            'json': json.dumps(analysis, indent=2)
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error generating report: {str(e)}',
            'error': str(e)
        }


def main():
    """Main entry point for command-line usage"""
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'report'
    
    result = handle_crm_report(command)
    
    if result['success']:
        print(result['message'])
        print("\n--- JSON DATA ---")
        print(result['json'])
    else:
        print(f"Error: {result['message']}")
        if 'error' in result:
            print(f"Details: {result['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
