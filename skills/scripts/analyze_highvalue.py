import json

with open('mock_data.json', 'r') as f:
    data = json.load(f)

leads = data.get('leads', [])
threshold = 1000000

high_value = [l for l in leads if float(l.get('deal_value', 0)) >= threshold]
qualified = [l for l in high_value if l.get('status') == 'Qualified']
new_leads = [l for l in high_value if l.get('status') == 'New']
at_risk = [l for l in high_value if l.get('status') == 'Lost']

print("\n=== HIGH-VALUE OPPORTUNITIES >=1M ===\n")
print(f"Total High-Value Deals: {len(high_value)}")
print(f"  Qualified (Ready to Close): {len(qualified)}")
print(f"  New High-Value Leads: {len(new_leads)}")
print(f"  At-Risk Deals: {len(at_risk)}")

qual_total = sum(float(l.get('deal_value', 0)) for l in qualified)
new_total = sum(float(l.get('deal_value', 0)) for l in new_leads)
risk_total = sum(float(l.get('deal_value', 0)) for l in at_risk)

print(f"\nTotal Value at Risk: Rs {risk_total:,.0f}")
print(f"Total Qualified Value: Rs {qual_total:,.0f}")
print(f"Total New Value: Rs {new_total:,.0f}")

print(f"\n=== RECOMMENDED ACTIONS ===\n")
if qualified:
    print(f"1. CLOSE QUALIFIED LEADS: {len(qualified)} deals ready")
    for l in qualified[:3]:
        print(f"   - {l.get('company_name')}: Rs {float(l.get('deal_value', 0)):,.0f}")

if new_leads:
    print(f"\n2. NURTURE NEW HIGH-VALUE: {len(new_leads)} new opportunities")
    for l in new_leads[:3]:
        print(f"   - {l.get('company_name')}: Rs {float(l.get('deal_value', 0)):,.0f}")

if at_risk:
    print(f"\n3. URGENT FOLLOW-UP: {len(at_risk)} lost deals to recover")
    for l in at_risk[:3]:
        print(f"   - {l.get('company_name')}: Rs {float(l.get('deal_value', 0)):,.0f}")

with open('alert_message.txt', 'w') as f:
    msg = f"CRM ALERT - High-Value Opportunities\n\n"
    msg += f"Qualified leads (ready to close): {len(qualified)} | Rs {qual_total:,.0f}\n"
    msg += f"New high-value leads: {len(new_leads)} | Rs {new_total:,.0f}\n"
    msg += f"At-risk deals: {len(at_risk)} | Rs {risk_total:,.0f}\n\n"
    msg += "ACTION: Review qualified deals for immediate close. Nurture new opportunities. Recover at-risk deals.\n"
    f.write(msg)
