# IT Support Ticketing Dashboard

**A Python-based IT support operations tool that simulates a ServiceNow ticket pipeline, generates management-ready Excel reports, and surfaces SLA compliance metrics — built to reflect real help desk workflows.**

---

## Why I Built This

In my role as a Customer Service Representative at the **City of Toronto (Parks, Forestry & Recreation)**, I work daily with **ServiceNow** to manage resident service requests, track case resolutions, and escalate to the right teams. I built this project to demonstrate how I think about IT support operations — not just closing tickets, but measuring performance, spotting patterns, and improving service delivery.

---

## What It Does

| Feature | Description |
|---|---|
| Ticket generator | Creates 50 realistic IT incidents across 8 categories (Hardware, Software, Network, VPN, etc.) |
| ServiceNow API module | Shows real REST API patterns — falls back to mock data without credentials |
| CSV export | Exports tickets in ServiceNow-style format for further analysis |
| Text report | Weekly performance summary: SLA compliance, resolution rate, agent load |
| Excel workbook | 3-sheet formatted report with colour-coded priorities and a bar chart |
| JSON summary | Machine-readable KPIs for integration with dashboards or monitoring tools |

---

## Sample Output

```
==============================
  IT SUPPORT WEEKLY PERFORMANCE REPORT
  Generated: 2024-06-09 10:22
==============================

SUMMARY
  Total Tickets:        50
  Open Tickets:         8
  Resolved Tickets:     37
  Resolution Rate:      74.0%
  SLA Compliance:       68.0%
  Avg Resolution Time:  21.4 hours

TICKETS BY CATEGORY
  Software               14  ##############
  Hardware               10  ##########
  Access/Permissions      8  ########
  Network                 6  ######
  ...
```

---

## Tools & Technologies

- **Python 3** — core logic, data processing, file I/O
- **ServiceNow** — REST API integration pattern (real + mock)
- **openpyxl** — Excel workbook generation with charts and conditional formatting
- **Active Directory** — referenced in ticket resolution workflows
- **CSV / JSON** — data export formats matching real enterprise reporting

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/yashsomaiya29/it-support-dashboard.git
cd it-support-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the main dashboard (generates tickets + text report + JSON)
python ticketing_dashboard.py

# 4. Generate the Excel report
python generate_excel_report.py

# 5. See the ServiceNow API integration
python servicenow_api.py
```

To connect to a **real ServiceNow instance**, set environment variables:
```bash
export SN_INSTANCE=your-instance-name
export SN_USERNAME=your-username
export SN_PASSWORD=your-password
```

---

## Output Files

```
data/
  tickets_export.csv          # 50 simulated tickets (ServiceNow export format)

reports/
  weekly_report.txt           # Management performance report
  dashboard_summary.json      # KPI summary (resolution rate, SLA compliance, etc.)
  IT_Support_Dashboard.xlsx   # Formatted Excel workbook with charts
```

---

## Project Structure

```
it-support-dashboard/
├── ticketing_dashboard.py    # Main: generates tickets, analyzes data, exports reports
├── generate_excel_report.py  # Excel workbook builder (3 sheets + bar chart)
├── servicenow_api.py         # ServiceNow REST API client (real + mock mode)
├── requirements.txt
├── data/
│   └── tickets_export.csv
└── reports/
    ├── weekly_report.txt
    ├── dashboard_summary.json
    └── IT_Support_Dashboard.xlsx
```

---

## What I Would Do Next

- **Live ServiceNow integration** — connect to a ServiceNow developer instance (free at developer.servicenow.com) and pull real data
- **Power BI / Tableau connector** — export the JSON summary to a live dashboard
- **Email alerts** — trigger automated SLA breach alerts via SMTP when P1 tickets exceed resolution time
- **Streamlit web UI** — wrap the dashboard in a web interface for non-technical managers
- **Azure deployment** — host as a scheduled Azure Function that runs every Monday morning

---

## About Me

**Yash Somaiya** — Cloud Computing & Digital Marketing | Open Work Permit

- Currently: CSR at City of Toronto using ServiceNow, Microsoft 365, ActiveNet daily
- Former: QA Analyst at Grim Panda Software (JIRA, Agile, iOS/Android testing)
- Built: [Straight Talk](https://straighttalk.lovable.app) — an AI-powered application using Claude API

📧 somaiya45yash@gmail.com | 🔗 [linkedin.com/in/yashsomaiya29](https://linkedin.com/in/yashsomaiya29)

---

*This project demonstrates real IT support operations thinking — not just Python skills.*
