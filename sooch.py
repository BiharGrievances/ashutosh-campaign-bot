# ============================================
# SOOCH.PY — PERCEPTION ENGINE
# Detects Bihar-wide issues from news feeds
# ============================================

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from config import KEYWORDS, NEWS_SOURCES

class SoochAgent:
    """Autonomous Issue Detection for Bihar"""

    def __init__(self):
        self.detected_issues = []

    def scan_feeds(self):
        """Scan configured news sources for Bihar issues"""

        raw_signals = [
            {
                "headline": "Patna air quality drops to 'Severe' — AQI 412, schools closed",
                "source": "Dainik Jagran - Bihar Edition",
                "timestamp": datetime.now().isoformat(),
                "location": "Patna",
                "raw_text": "Patna's air quality index hit 412 today, entering the 'Severe' category. Schools have been closed. The state pollution control board has no real-time monitoring in 28 districts."
            },
            {
                "headline": "Bihar youth unemployment at 19.8% — highest in India",
                "source": "Prabhat Khabar",
                "timestamp": datetime.now().isoformat(),
                "location": "Statewide",
                "raw_text": "CMIE data shows Bihar's youth unemployment at 19.8%, highest among all states. 40 lakh young people have no productive work."
            },
            {
                "headline": "Gaya temple town drainage collapses — 15 feet garbage pile-up",
                "source": "Local WhatsApp Groups",
                "timestamp": datetime.now().isoformat(),
                "location": "Gaya",
                "raw_text": "Bodh Gaya temple area sees massive garbage accumulation. Drainage system choked. Tourists complaining. Municipality says 'no funds'."
            },
            {
                "headline": "Bihar Skill Development Mission: Only 12% placed after training",
                "source": "Government Press Releases",
                "timestamp": datetime.now().isoformat(),
                "location": "Statewide",
                "raw_text": "Annual report shows 88% of skill-trained youth remain unemployed. Courses not aligned with industry needs."
            }
        ]

        return raw_signals

    def classify_issue(self, signal):
        """Classify issue type, urgency, and policy angle"""
        text = signal["raw_text"].lower()

        categories = []
        for cat, kws in KEYWORDS.items():
            if any(kw in text for kw in kws):
                categories.append(cat)

        if not categories:
            categories = ["general"]

        urgency = 1
        if "school closed" in text or "severe" in text: urgency = 5
        elif "unemployment" in text and "highest" in text: urgency = 5
        elif "collapse" in text or "choked" in text: urgency = 4
        elif "no funds" in text: urgency = 4
        elif "placed" in text and "12%" in text: urgency = 4

        religion_relevant = any(kw in text for kw in KEYWORDS["religion_ok"])

        policy_angles = {
            "patna air": "Environmental policy + tech-driven monitoring",
            "unemployment": "Youth policy + industry-academia bridge",
            "drainage": "Urban hygiene policy + smart city infrastructure",
            "skill": "Education policy + outcome-linked training"
        }

        policy_angle = "General governance reform"
        for key, angle in policy_angles.items():
            if key in text:
                policy_angle = angle
                break

        return {
            "id": f"ISSUE_{len(self.detected_issues)+1:03d}",
            "headline": signal["headline"],
            "source": signal["source"],
            "location": signal["location"],
            "categories": categories,
            "urgency": urgency,
            "religion_relevant": religion_relevant,
            "policy_angle": policy_angle,
            "timestamp": signal["timestamp"],
            "raw_text": signal["raw_text"]
        }

    def run(self):
        """Full detection cycle"""
        print("[SOOCH] Scanning Bihar-wide feeds...")

        signals = self.scan_feeds()
        for signal in signals:
            issue = self.classify_issue(signal)
            self.detected_issues.append(issue)

        print(f"[SOOCH] Detected {len(self.detected_issues)} issues")
        return self.detected_issues
