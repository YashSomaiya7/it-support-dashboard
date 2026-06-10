"""
IT Support Ticketing Dashboard
Author: Yash Somaiya
Tools: Python, ServiceNow (simulated), Excel, Data Analysis
Purpose: Simulates a real help desk ticket pipeline and generates management reports
"""

import json
import random
import csv
from datetime import datetime, timedelta
from collections import defaultdict
import os

# ─── Ticket Data Generator (simulates ServiceNow export) ───────────────────────

CATEGORIES = ["Hardware", "Software", "Network", "Access/Permissions", "Email", "Printer", "VPN", "Other"]
PRIORITIES  = ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"]
STATUSES    = ["Open", "In Progress", "Resolved", "Closed", "Pending User"]
AGENTS      = ["Yash Somaiya", "Alex Chen", "Maria Lopez", "Jordan Smith", "Priya Patel"]
DEPARTMENTS = ["Finance", "HR", "IT", "Operations", "Marketing", "Legal", "Facilities"]

ISSUE_TEMPLATES = {
    "Hardware":           ["Laptop not turning on", "Monitor flickering", "Keyboard unresponsive", "Docking station issue"],
    "Software":           ["Application crashing on launch", "Software license expired", "Unable to install update", "Excel freezing"],
    "Network":            ["No internet connection", "Slow network performance", "Unable to connect to VPN", "WiFi dropping"],
    "Access/Permissions": ["Cannot access shared drive", "Password reset required", "New user account setup", "MFA not working"],
    "Email":              ["Outlook not syncing", "Cannot send attachments", "Email account locked", "Spam filter blocking emails"],
    "Printer":            ["Printer offline", "Print job stuck in queue", "Unable to find printer on network", "Paper jam error"],
    "VPN":                ["VPN connection timeout", "Two-factor auth failure", "VPN client not installing", "Remote access denied"],
    "Other":              ["General IT inquiry", "Software recommendation request", "Data backup question", "IT policy clarification"],
}

RESOLUTIONS = {
    "Hardware":           "Dispatched technician. Hardware replaced/repaired.",
    "Software":           "Reinstalled application and applied latest patch.",
    "Network":            "Reset network adapter. Escalated to network team if persistent.",
    "Access/Permissions": "Reset credentials via Active Directory. Verified MFA enrollment.",
    "Email":              "Reconfigured Outlook profile. Cleared cache.",
    "Printer":            "Cleared print queue. Reconnected printer via IP address.",
    "VPN":                "Updated VPN client. Verified user profile in Azure AD.",
    "Other":              "Provided documentation and guidance. Closed after user confirmation.",
}

def random_date(start_days_ago=30):
    start = datetime.now() - timedelta(days=start_days_ago)
    random_seconds = random.randint(0, start_days_ago * 86400)
    return start + timedelta(seconds=random_seconds)

def generate_tickets(count=50):
    tickets = []
    for i in range(1, count + 1):
        category   = random.choice(CATEGORIES)
        priority   = random.choices(PRIORITIES, weights=[5, 15, 50, 30])[0]
        status     = random.choices(STATUSES, weights=[10, 20, 35, 30, 5])[0]
        created_at = random_date(30)
        agent      = random.choice(AGENTS)
        department = random.choice(DEPARTMENTS)

        if status in ["Resolved", "Closed"]:
            base_hours = {"P1 - Critical": 2, "P2 - High": 8, "P3 - Medium": 24, "P4 - Low": 72}
            sla_hours  = base_hours[priority]
            actual_hrs = random.uniform(sla_hours * 0.5, sla_hours * 2.5)
            resolved_at = created_at + timedelta(hours=actual_hrs)
            resolution_time_hrs = round(actual_hrs, 1)
            met_sla = actual_hrs <= sla_hours
            resolution_note = RESOLUTIONS[category]
        else:
            resolved_at = None
            resolution_time_hrs = None
            met_sla = None
            resolution_note = ""

        tickets.append({
            "ticket_id":           f"INC{str(i).zfill(5)}",
            "created_at":          created_at.strftime("%Y-%m-%d %H:%M"),
            "resolved_at":         resolved_at.strftime("%Y-%m-%d %H:%M") if resolved_at else "",
            "category":            category,
            "priority":            priority,
            "status":              status,
            "issue":               random.choice(ISSUE_TEMPLATES[category]),
            "department":          department,
            "assigned_agent":      agent,
            "resolution_time_hrs": resolution_time_hrs if resolution_time_hrs else "",
            "met_sla":             ("Yes" if met_sla else "No") if met_sla is not None else "N/A",
            "resolution_note":     resolution_note,
            "satisfaction_score":  random.randint(3, 5) if status in ["Resolved", "Closed"] else "",
        })
    return tickets

# ─── Analysis Functions ─────────────────────────────────────────────────────────

def analyze_tickets(tickets):
    total = len(tickets)
    resolved = [t for t in tickets if t["status"] in ["Resolved", "Closed"]]
    open_tickets = [t for t in tickets if t["status"] == "Open"]
    sla_tickets = [t for t in resolved if t["met_sla"] == "Yes"]

    by_category = defaultdict(int)
    by_priority = defaultdict(int)
    by_agent    = defaultdict(int)
    by_dept     = defaultdict(int)
    by_status   = defaultdict(int)

    for t in tickets:
        by_category[t["category"]] += 1
        by_priority[t["priority"]] += 1
        by_agent[t["assigned_agent"]] += 1
        by_dept[t["department"]] += 1
        by_status[t["status"]] += 1

    avg_resolution = 0
    if resolved:
        times = [float(t["resolution_time_hrs"]) for t in resolved if t["resolution_time_hrs"]]
        avg_resolution = round(sum(times) / len(times), 1) if times else 0

    return {
        "total_tickets":        total,
        "open_tickets":         len(open_tickets),
        "resolved_tickets":     len(resolved),
        "resolution_rate_pct":  round(len(resolved) / total * 100, 1),
        "sla_compliance_pct":   round(len(sla_tickets) / len(resolved) * 100, 1) if resolved else 0,
        "avg_resolution_hrs":   avg_resolution,
        "by_category":          dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
        "by_priority":          dict(by_priority),
        "by_agent":             dict(sorted(by_agent.items(), key=lambda x: x[1], reverse=True)),
        "by_department":        dict(sorted(by_dept.items(), key=lambda x: x[1], reverse=True)),
        "by_status":            dict(by_status),
    }

# ─── CSV Export (simulates ServiceNow export format) ───────────────────────────

def export_to_csv(tickets, filepath="data/tickets_export.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = tickets[0].keys()
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)
    print(f"  [OK] Ticket data exported: {filepath}")

# ─── Text Report Generator ──────────────────────────────────────────────────────

def generate_report(stats, filepath="reports/weekly_report.txt"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "=" * 60,
        "  IT SUPPORT WEEKLY PERFORMANCE REPORT",
        f"  Generated: {now}",
        "=" * 60,
        "",
        "SUMMARY",
        "-" * 40,
        f"  Total Tickets:        {stats['total_tickets']}",
        f"  Open Tickets:         {stats['open_tickets']}",
        f"  Resolved Tickets:     {stats['resolved_tickets']}",
        f"  Resolution Rate:      {stats['resolution_rate_pct']}%",
        f"  SLA Compliance:       {stats['sla_compliance_pct']}%",
        f"  Avg Resolution Time:  {stats['avg_resolution_hrs']} hours",
        "",
        "TICKETS BY CATEGORY",
        "-" * 40,
    ]
    for cat, count in stats["by_category"].items():
        bar = "#" * (count // 1)
        lines.append(f"  {cat:<22} {count:>3}  {bar}")

    lines += ["", "TICKETS BY PRIORITY", "-" * 40]
    for pri, count in stats["by_priority"].items():
        lines.append(f"  {pri:<22} {count:>3}")

    lines += ["", "AGENT PERFORMANCE", "-" * 40]
    for agent, count in stats["by_agent"].items():
        lines.append(f"  {agent:<22} {count:>3} tickets handled")

    lines += ["", "TOP DEPARTMENTS SUBMITTING TICKETS", "-" * 40]
    for dept, count in stats["by_department"].items():
        lines.append(f"  {dept:<22} {count:>3}")

    lines += ["", "RECOMMENDATIONS", "-" * 40,
        "  1. Access/Permissions tickets are high — consider AD self-service portal.",
        "  2. P1 SLA compliance should be reviewed if below 90%.",
        "  3. Hardware tickets spiking in Finance — schedule preventive maintenance.",
        "  4. Consider knowledge base articles for top recurring issues.",
        "",
        "=" * 60,
        "  Report generated by IT Support Dashboard v1.0",
        "  Author: Yash Somaiya | Tools: Python, ServiceNow, Excel",
        "=" * 60,
    ]

    with open(filepath, "w") as f:
        f.write("\n".join(lines))
    print(f"  [OK] Weekly report saved: {filepath}")
    return "\n".join(lines)

# ─── JSON Summary Export ────────────────────────────────────────────────────────

def export_json_summary(stats, filepath="reports/dashboard_summary.json"):
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  [OK] JSON summary saved: {filepath}")

# ─── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 60)
    print("  IT Support Ticketing Dashboard — Starting...")
    print("=" * 60 + "\n")

    print("Step 1: Generating simulated ServiceNow ticket data...")
    tickets = generate_tickets(50)

    print("Step 2: Exporting ticket data to CSV...")
    export_to_csv(tickets, "data/tickets_export.csv")

    print("Step 3: Analyzing ticket metrics...")
    stats = analyze_tickets(tickets)

    print("Step 4: Generating weekly performance report...")
    report = generate_report(stats, "reports/weekly_report.txt")

    print("Step 5: Exporting dashboard JSON summary...")
    export_json_summary(stats, "reports/dashboard_summary.json")

    print("\n" + "=" * 60)
    print("  DASHBOARD SUMMARY PREVIEW")
    print("=" * 60)
    print(f"\n  Total Tickets      : {stats['total_tickets']}")
    print(f"  Open               : {stats['open_tickets']}")
    print(f"  Resolved           : {stats['resolved_tickets']}")
    print(f"  Resolution Rate    : {stats['resolution_rate_pct']}%")
    print(f"  SLA Compliance     : {stats['sla_compliance_pct']}%")
    print(f"  Avg Resolution Time: {stats['avg_resolution_hrs']} hrs")
    print(f"\n  Top Category: {list(stats['by_category'].keys())[0]}")
    print(f"  Busiest Agent: {list(stats['by_agent'].keys())[0]}")
    print("\n  All files saved to /data and /reports folders.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
