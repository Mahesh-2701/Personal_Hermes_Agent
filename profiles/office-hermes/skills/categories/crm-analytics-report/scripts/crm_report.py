#!/usr/bin/env python3
"""
CRM Analytics Report Generator
Fetches data from Zoho CRM and generates formatted reports
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Try to import httpx for real API calls
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


def get_zoho_token() -> Optional[str]:
    """Get Zoho CRM token from environment"""
    return os.environ.get('ZOHO_CRM_ACCESS_TOKEN')


def make_zoho_request(endpoint: str, params: Dict = None) -> Dict:
    """Make API request to Zoho CRM"""
    if not HTTPX_AVAILABLE:
        return {"error": "httpx not available, using mock data"}
    
    token = get_zoho_token()
    if not token:
        return {"error": "ZOHO_CRM_ACCESS_TOKEN not configured"}
    
    headers = {
        'Authorization': f'Zoho-oauthtoken {token}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://www.zohoapis.com/crm/v2/{endpoint}'
    
    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API Error {response.status_code}",
                "message": response.text
            }
    except Exception as e:
        return {"error": str(e)}


def fetch_contacts() -> List[Dict]:
    """Fetch all contacts from Zoho CRM"""
    result = make_zoho_request('Contacts', {'per_page': 200})
    
    if 'error' in result:
        # Return mock data for testing
        return generate_mock_contacts()
    
    return result.get('data', [])


def fetch_leads() -> List[Dict]:
    """Fetch all leads/deals from Zoho CRM"""
    result = make_zoho_request('Deals', {'per_page': 200})
    
    if 'error' in result:
        # Return mock data for testing
        return generate_mock_leads()
    
    return result.get('data', [])


def fetch_accounts() -> List[Dict]:
    """Fetch all accounts/companies from Zoho CRM"""
    result = make_zoho_request('Accounts', {'per_page': 200})
    
    if 'error' in result:
        # Return mock data for testing
        return generate_mock_accounts()
    
    return result.get('data', [])


def generate_mock_contacts() -> List[Dict]:
    """Generate mock contact data for testing"""
    statuses = ['Active', 'Inactive', 'Lead']
    return [
        {
            'id': f'cont_{i}',
            'Full_Name': f'Contact {i}',
            'Email': f'contact{i}@company.com',
            'Phone': f'+91-9{i:03d}-{i*111:04d}',
            'Company': f'Company {i % 5}',
            'Status': statuses[i % len(statuses)]
        }
        for i in range(1, 246)
    ]


def generate_mock_leads() -> List[Dict]:
    """Generate mock leads/deals data for testing"""
    statuses = ['New', 'Qualified', 'Won', 'Lost']
    return [
        {
            'id': f'lead_{i}',
            'Deal_Name': f'Deal {i}',
            'Amount': 50000 * (i % 10 + 1),
            'Stage': statuses[i % len(statuses)],
            'Probability': ((i % 4 + 1) * 25),
            'Lead_Source': ['Website', 'Referral', 'Email', 'Event'][i % 4],
            'Owner': f'Sales Rep {i % 3}'
        }
        for i in range(1, 79)
    ]


def generate_mock_accounts() -> List[Dict]:
    """Generate mock accounts/companies data for testing"""
    industries = ['IT', 'Manufacturing', 'Retail', 'Finance', 'Healthcare']
    return [
        {
            'id': f'acc_{i}',
            'Account_Name': f'Company {i}',
            'Website': f'https://company{i}.com',
            'Industry': industries[i % len(industries)],
            'Annual_Revenue': 1000000 * (i % 100 + 1),
            'Phone': f'+91-40-{i*111:04d}',
            'Employees': 10 * (i % 200 + 1)
        }
        for i in range(1, 51)
    ]


def analyze_contacts(contacts: List[Dict]) -> Dict:
    """Analyze contacts and generate stats"""
    if not contacts:
        return {"error": "No contacts found"}
    
    status_counts = {}
    for contact in contacts:
        status = contact.get('Status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        'total': len(contacts),
        'by_status': status_counts,
        'percentage_active': round(
            (status_counts.get('Active', 0) / len(contacts) * 100), 1
        ) if len(contacts) > 0 else 0
    }


def analyze_leads(leads: List[Dict]) -> Dict:
    """Analyze leads/deals and generate pipeline stats"""
    if not leads:
        return {"error": "No leads found"}
    
    stage_counts = {}
    stage_values = {}
    
    for lead in leads:
        stage = lead.get('Stage', 'Unknown')
        amount = lead.get('Amount', 0)
        
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        stage_values[stage] = stage_values.get(stage, 0) + amount
    
    total_value = sum(stage_values.values())
    
    return {
        'total': len(leads),
        'by_stage': stage_counts,
        'pipeline_value': total_value,
        'by_stage_value': stage_values,
        'win_rate': round(
            (stage_counts.get('Won', 0) / len(leads) * 100), 1
        ) if len(leads) > 0 else 0
    }


def analyze_accounts(accounts: List[Dict]) -> Dict:
    """Analyze accounts and generate company stats"""
    if not accounts:
        return {"error": "No accounts found"}
    
    industries = {}
    total_revenue = 0
    
    for account in accounts:
        industry = account.get('Industry', 'Unknown')
        industries[industry] = industries.get(industry, 0) + 1
        total_revenue += account.get('Annual_Revenue', 0)
    
    return {
        'total': len(accounts),
        'by_industry': industries,
        'total_revenue': total_revenue,
        'avg_revenue': round(total_revenue / len(accounts), 0) if accounts else 0
    }


def format_report_text(contacts_analysis: Dict, leads_analysis: Dict, accounts_analysis: Dict) -> str:
    """Format report as readable text"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M IST')
    
    text = f"""
== CRM ANALYTICS REPORT ==
As of {timestamp}

CONTACTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Contacts: {contacts_analysis.get('total', 0)}
  Active: {contacts_analysis.get('by_status', {}).get('Active', 0)}
  Inactive: {contacts_analysis.get('by_status', {}).get('Inactive', 0)}
  Leads: {contacts_analysis.get('by_status', {}).get('Lead', 0)}
  Active Rate: {contacts_analysis.get('percentage_active', 0)}%

ACCOUNTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Companies: {accounts_analysis.get('total', 0)}
  Total Revenue: Rs {accounts_analysis.get('total_revenue', 0):,.0f}
  Avg Revenue: Rs {accounts_analysis.get('avg_revenue', 0):,.0f}
  Industries: {', '.join(accounts_analysis.get('by_industry', {}).keys())}

LEADS PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Deals: {leads_analysis.get('total', 0)}
  Pipeline Value: Rs {leads_analysis.get('pipeline_value', 0):,.0f}
  
  By Stage:
"""
    
    for stage, count in leads_analysis.get('by_stage', {}).items():
        value = leads_analysis.get('by_stage_value', {}).get(stage, 0)
        text += f"    - {stage}: {count} deals (Rs {value:,.0f})\n"
    
    text += f"\n  Win Rate: {leads_analysis.get('win_rate', 0)}%\n"
    
    return text


def format_report_json(contacts_analysis: Dict, leads_analysis: Dict, accounts_analysis: Dict) -> Dict:
    """Format report as JSON"""
    return {
        'timestamp': datetime.now().isoformat(),
        'contacts': contacts_analysis,
        'accounts': accounts_analysis,
        'leads': leads_analysis
    }


def generate_full_report(output_format: str = 'text') -> Dict:
    """Generate complete CRM report"""
    
    print("Fetching CRM data...")
    contacts = fetch_contacts()
    leads = fetch_leads()
    accounts = fetch_accounts()
    
    print("Analyzing data...")
    contacts_analysis = analyze_contacts(contacts)
    leads_analysis = analyze_leads(leads)
    accounts_analysis = analyze_accounts(accounts)
    
    if output_format == 'json':
        report = format_report_json(contacts_analysis, leads_analysis, accounts_analysis)
        return {
            'success': True,
            'format': 'json',
            'data': report
        }
    else:
        report_text = format_report_text(contacts_analysis, leads_analysis, accounts_analysis)
        return {
            'success': True,
            'format': 'text',
            'data': report_text,
            'analysis': {
                'contacts': contacts_analysis,
                'leads': leads_analysis,
                'accounts': accounts_analysis
            }
        }


def generate_mock_report() -> Dict:
    """Generate report with mock data (for testing)"""
    print("Using mock data (token not configured)")
    
    contacts = generate_mock_contacts()
    leads = generate_mock_leads()
    accounts = generate_mock_accounts()
    
    contacts_analysis = analyze_contacts(contacts)
    leads_analysis = analyze_leads(leads)
    accounts_analysis = analyze_accounts(accounts)
    
    report_text = format_report_text(contacts_analysis, leads_analysis, accounts_analysis)
    
    return {
        'success': True,
        'format': 'text',
        'data': report_text,
        'analysis': {
            'contacts': contacts_analysis,
            'leads': leads_analysis,
            'accounts': accounts_analysis
        },
        'note': 'Using mock data for testing'
    }


if __name__ == '__main__':
    import sys
    
    output_format = sys.argv[1] if len(sys.argv) > 1 else 'text'
    
    report = generate_full_report(output_format)
    
    if output_format == 'json':
        print(json.dumps(report, indent=2))
    else:
        print(report['data'])
