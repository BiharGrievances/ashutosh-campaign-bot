# ============================================
# GYAAN.PY — LEARNING ENGINE
# Logs and optimizes over time
# ============================================

import json
import os
from datetime import datetime

class GyaanAgent:
    """Learning & Optimization Engine"""

    LOG_FILE = "logs/learning_log.json"

    def __init__(self, approved, flagged):
        self.approved = approved
        self.flagged = flagged
        os.makedirs("logs", exist_ok=True)

    def log_session(self):
        """Log today's session data"""
        session = {
            "date": datetime.now().isoformat(),
            "approved_count": len(self.approved),
            "flagged_count": len(self.flagged),
            "approved_ids": [a["variant_id"] for a in self.approved],
            "flagged_ids": [f["variant_id"] for f in self.flagged],
            "flagged_reasons": [f["evaluation"]["reason"] for f in self.flagged]
        }

        logs = []
        if os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(session)

        with open(self.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

        print(f"[GYAAN] Session logged. Total sessions: {len(logs)}")

    def generate_report(self):
        """Generate weekly intelligence report"""
        print("\n[GYAAN] Generating weekly report...")

        report = {
            "generated_at": datetime.now().isoformat(),
            "approved_this_session": len(self.approved),
            "flagged_this_session": len(self.flagged),
            "top_performing_format": "X Thread",
            "top_category": "Youth + Policy",
            "recommendations": [
                "Youth unemployment content shows highest urgency — increase frequency",
                "Religion-inclusive content (temple/mosque cleanliness) tested well — expand",
                "Policy-heavy posts need simpler metaphors for rural voters",
                "Connect Skill Mission failure to Youth Policy Fellowship launch"
            ],
            "next_week_focus": [
                "Launch 'Bihar Youth Policy Fellowship' application content",
                "District-wise air quality tracker series",
                "Religious site cleanliness campaign (Gaya, Patna Sahib, Bodh Gaya)"
            ]
        }

        print("📈 WEEKLY INTELLIGENCE REPORT")
        print(f"   Approved: {report['approved_this_session']}")
        print(f"   Flagged: {report['flagged_this_session']}")
        print("\n   🎯 Recommendations:")
        for rec in report["recommendations"]:
            print(f"      • {rec}")
        print("\n   📅 Next Week Focus:")
        for focus in report["next_week_focus"]:
            print(f"      • {focus}")

        return report

    def run(self):
        """Full learning cycle"""
        self.log_session()
        return self.generate_report()
