"""
ServiceNow API Integration Module
Author: Yash Somaiya

This module shows how you would connect to a REAL ServiceNow instance.
In this portfolio demo, it falls back to mock data when no credentials are set.
This demonstrates understanding of REST API patterns used in real IT environments.

Usage:
    from servicenow_api import ServiceNowClient
    client = ServiceNowClient(instance="your-instance", username="user", password="pass")
    tickets = client.get_incidents(limit=50)
"""

import json
import os
from datetime import datetime

# In a real environment, these come from environment variables (never hardcoded)
SN_INSTANCE = os.environ.get("SN_INSTANCE", "")
SN_USERNAME = os.environ.get("SN_USERNAME", "")
SN_PASSWORD = os.environ.get("SN_PASSWORD", "")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class ServiceNowClient:
    """
    Client for ServiceNow REST API.
    Falls back to mock data if credentials are not configured.

    Real ServiceNow REST API docs:
    https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI
    """

    def __init__(self, instance=None, username=None, password=None):
        self.instance = instance or SN_INSTANCE
        self.username = username or SN_USERNAME
        self.password = password or SN_PASSWORD
        self.base_url = f"https://{self.instance}.service-now.com/api/now" if self.instance else None
        self.is_mock  = not (self.instance and self.username and self.password)

        if self.is_mock:
            print("[INFO] ServiceNow credentials not set. Running in MOCK mode.")
            print("[INFO] To connect to real ServiceNow, set environment variables:")
            print("       SN_INSTANCE, SN_USERNAME, SN_PASSWORD")
        else:
            print(f"[INFO] Connected to ServiceNow instance: {self.instance}")

    def get_incidents(self, limit=50, state=None, priority=None):
        """
        Fetch incidents from ServiceNow.
        Real endpoint: GET /api/now/table/incident

        Params:
            limit    — max records to return
            state    — filter by state (1=New, 2=In Progress, 6=Resolved, 7=Closed)
            priority — filter by priority (1=Critical, 2=High, 3=Medium, 4=Low)
        """
        if self.is_mock or not REQUESTS_AVAILABLE:
            return self._mock_incidents(limit)

        params = {
            "sysparm_limit":  limit,
            "sysparm_fields": "number,short_description,category,priority,state,assigned_to,sys_created_on,resolved_at,close_notes",
        }
        if state:
            params["state"] = state
        if priority:
            params["priority"] = priority

        try:
            response = requests.get(
                f"{self.base_url}/table/incident",
                auth=(self.username, self.password),
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return self._normalize_real_response(response.json().get("result", []))
        except Exception as e:
            print(f"[WARN] API call failed: {e}. Falling back to mock data.")
            return self._mock_incidents(limit)

    def create_incident(self, short_description, category, priority=3, caller_id="guest"):
        """
        Create a new incident ticket.
        Real endpoint: POST /api/now/table/incident
        """
        if self.is_mock or not REQUESTS_AVAILABLE:
            print(f"[MOCK] Would create ticket: '{short_description}' | Cat: {category} | Priority: P{priority}")
            return {"ticket_id": "INC0099999", "status": "mock_created"}

        payload = {
            "short_description": short_description,
            "category":          category,
            "priority":          str(priority),
            "caller_id":         caller_id,
        }
        try:
            response = requests.post(
                f"{self.base_url}/table/incident",
                auth=(self.username, self.password),
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            result = response.json().get("result", {})
            print(f"[OK] Ticket created: {result.get('number')}")
            return {"ticket_id": result.get("number"), "status": "created"}
        except Exception as e:
            print(f"[ERROR] Could not create ticket: {e}")
            return {"error": str(e)}

    def update_incident(self, ticket_number, state=None, resolution_notes=None):
        """
        Update an existing incident (e.g. mark resolved).
        Real endpoint: PATCH /api/now/table/incident/{sys_id}
        """
        if self.is_mock or not REQUESTS_AVAILABLE:
            print(f"[MOCK] Would update ticket {ticket_number}: state={state}")
            return {"status": "mock_updated"}

        payload = {}
        if state:
            payload["state"] = str(state)
        if resolution_notes:
            payload["close_notes"] = resolution_notes
            payload["close_code"]  = "Solved (Permanently)"

        print(f"[INFO] PATCH to /table/incident with payload: {payload}")
        return {"status": "would_patch_real_api"}

    def _normalize_real_response(self, records):
        """Map real ServiceNow field names to our internal format."""
        normalized = []
        for r in records:
            normalized.append({
                "ticket_id":      r.get("number", ""),
                "created_at":     r.get("sys_created_on", ""),
                "resolved_at":    r.get("resolved_at", ""),
                "category":       r.get("category", {}).get("value", "") if isinstance(r.get("category"), dict) else r.get("category", ""),
                "priority":       r.get("priority", {}).get("display_value", "") if isinstance(r.get("priority"), dict) else r.get("priority", ""),
                "status":         r.get("state", {}).get("display_value", "") if isinstance(r.get("state"), dict) else r.get("state", ""),
                "issue":          r.get("short_description", ""),
                "assigned_agent": r.get("assigned_to", {}).get("display_value", "") if isinstance(r.get("assigned_to"), dict) else "",
                "resolution_note": r.get("close_notes", ""),
            })
        return normalized

    def _mock_incidents(self, limit):
        """Return mock data that mirrors real ServiceNow structure."""
        print(f"[MOCK] Returning {limit} simulated incidents.")
        # In real usage this calls the main ticket generator
        try:
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from ticketing_dashboard import generate_tickets
            return generate_tickets(limit)
        except ImportError:
            return []


# ─── Demonstration ──────────────────────────────────────────────────────────────

def demo():
    print("\n" + "=" * 60)
    print("  ServiceNow API Integration — Demo")
    print("=" * 60 + "\n")

    client = ServiceNowClient()

    print("\n[1] Fetching incidents...")
    tickets = client.get_incidents(limit=5)
    for t in tickets[:3]:
        print(f"    {t['ticket_id']} | {t['priority']} | {t['category']} | {t['status']}")

    print("\n[2] Creating a new incident...")
    result = client.create_incident(
        short_description="User cannot access shared drive after password reset",
        category="Access/Permissions",
        priority=2
    )
    print(f"    Result: {result}")

    print("\n[3] Updating an incident...")
    result = client.update_incident(
        ticket_number="INC00001",
        state=6,
        resolution_notes="Reset AD permissions. User confirmed access restored."
    )
    print(f"    Result: {result}")

    print("\n" + "=" * 60)
    print("  In a real environment, set these env variables to go live:")
    print("  export SN_INSTANCE=your-company-dev")
    print("  export SN_USERNAME=admin")
    print("  export SN_PASSWORD=yourpassword")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    demo()
